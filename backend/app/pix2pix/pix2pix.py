import os

import albumentations as A
import numpy as np
import SimpleITK as sitk
from lungmask import mask as unet_mask
from skimage.transform import resize
from tensorflow.keras.models import model_from_json
from utils import *


class Pix2Pix:
    """Модель использующая pix2pix архитектуру для генерации по скетчу с лёгким изображения.

    Args:
        model_h5_path : str : путь к файлу с весами, расширения h5
        model_json_path : str : путь к файлу с метаданными модели, расширения json
        original_masks_dir : str : путь к папке с масками, у всех файлов в папке должно быть расширение nii
    Methods:
        inference : открывает dicom файлы (N, H, W) и генерирует по нему, возвращая КТ-скан (N, H, W) и маску (N, H, W)
        ...
    """

    def __init__(self, model_h5_path, model_json_path, original_masks_dir) -> None:
        self.W = 512
        self.H = 512
        with open(model_json_path, "r") as f:
            self.model = model_from_json(f.read())
        self.model.load_weights(model_h5_path)
        self.original_masks_dir = original_masks_dir

    def inference(self, dicom_path, original_mask=None):
        """Открывает dicom файлы (N, H, W) и генерирует по нему, возвращая
        сгенерированный КТ-скан (N, H, W) и маску (N, H, W).

        Args:
            dicom_path : str : путь к папке с dicom файлами.
            original_mask : ndarray : размер (K, 512, 512), куб с масками по которые будут браться для модели.
                Note. можно открыть original mask с помощью функции из модуля utils read_image.
        Return:
            norm_rec_gen : ndarray[N, H, W] : КТ-скан со сгенерированными поверх него поражениями COVID.
            rec_masks : ndarray[N, H, W] : Маска это КТ-снимка с поражениями.
        """
        image = load_dicom(dicom_path)
        lung = self.segmentation_lung(image)

        image = sitk.GetArrayFromImage(image)

        if original_mask is not None:
            original_mask = read_image(original_mask)
        else:
            original_mask = self.get_random_original_mask(self.original_masks_dir)

        sketch, gen_masks = self.generate_sketch(image, lung, original_mask)

        pred = self.multi_prediction(sketch, self.model)
        rec_gen, rec_masks = self.recover_synthetic_image(
            pred, normalize(image), lung, gen_masks, self.get_masked_layers(lung)
        )

        norm_rec_gen = unnormalize(rec_gen, np.min(image), np.max(image))
        rec_masks = self.get_lung(rec_masks, lung)
        return norm_rec_gen, np.uint16(rec_masks > 0)

    # ---------------------
    # Normalization
    # ---------------------

    def normalize_nn(self, input_image):
        input_image = (input_image / 127.5) - 1
        return input_image

    def unnormalize_nn(self, x):
        return (1 + x) / 2

    # ---------------------
    # Generate sketch
    # ---------------------

    def segmentation_lung(self, SimpleITK_image):
        model = unet_mask.get_model("unet", "LTRCLobes")
        segmentation = unet_mask.apply(SimpleITK_image, model)
        return segmentation

    def get_lung(self, image, lung_mask):
        return image * (lung_mask > 0)

    def get_random_original_mask(self, masks_path):
        for root, dirs, files in os.walk(masks_path):
            f = np.random.choice(files)
            return read_image(os.path.join(root, f))

    def get_masked_layers(self, mask):
        layers = np.arange(mask.shape[0])
        not_empty_layers = layers[~np.all(mask == 0, axis=(1, 2))]
        return not_empty_layers

    def generate_slice_sketch(self, cropped_lung, original_mask=None):
        aug = A.OneOf(
            [
                A.GridDistortion(p=0.5),
                A.ElasticTransform(
                    alpha=120,
                    sigma=120 * 0.13,
                    alpha_affine=120 * 0.1,
                    border_mode=0,
                    p=0.2,
                ),
                A.OpticalDistortion(
                    distort_limit=0.7, shift_limit=0.4, border_mode=0, p=0.3
                ),
            ]
        )

        augmented = aug(image=original_mask, mask=original_mask)

        mask = np.zeros(cropped_lung.shape)
        mask[:, :, 1] += augmented["mask"]

        new_image = np.copy(cropped_lung)
        new_image[np.repeat(mask[:, :, 1][..., np.newaxis], 3, axis=2) > 0] = 0
        new_image += np.uint8(mask * 255) * (cropped_lung > 0)

        return new_image, augmented["mask"]

    def get_lesion(self, original_mask):
        layers = self.get_masked_layers(original_mask > 0)
        idx = np.random.choice(layers)
        return original_mask[idx]

    def generate_sketch(self, image, lung, original_mask=None, size=(512, 512)):
        sektches = []
        gen_masks = []
        for i in self.get_masked_layers(lung > 0):
            image_slice = image[i]
            lung_slice = lung[i]
            mask_slice = self.get_lesion(original_mask)
            cropped_lung = self.get_lung(image2gray255(image_slice), lung_slice)
            cropped_lung = gray2rgb255(cropped_lung)
            if cropped_lung.shape[:2] != size:
                cropped_lung = resize_cube(cropped_lung, size)
            sketch, gen_mask = self.generate_slice_sketch(cropped_lung, mask_slice)
            sektches.append(sketch)
            gen_masks.append(gen_mask)
        return sektches, gen_masks

    # ---------------------
    # Prediction
    # ---------------------
    def single_prediction(self, src_img, model):
        im = self.normalize_nn(src_img)
        im = np.expand_dims(im, axis=0)
        pred = model(im, training=True)
        return self.unnormalize_nn(pred.numpy())

    def multi_prediction(self, imgs, model):
        results = []
        for img in imgs:
            results.append(self.single_prediction(img, model))
        return np.concatenate(results, axis=0)

    # ---------------------
    # Postprocessing
    # ---------------------
    def lung_with_bg(self, image, synthetic, lung_mask):
        return image * (1 - (lung_mask > 0)) + synthetic

    def recover_synthetic_image(
        self, gen_image, source_image, source_lung, gen_masks, gen_layers
    ):
        images = []
        masks = []
        start_size = source_image.shape[1:][::-1]
        j = 0
        for i in range(source_image.shape[0]):
            if i in gen_layers:
                g_im = gen_image[j]
                g_im = rgb2gray(g_im)
                reconstuct_gen_image = resize(g_im, start_size)
                images.append(
                    self.lung_with_bg(
                        source_image[i], reconstuct_gen_image, source_lung[i]
                    )[np.newaxis]
                )
                masks.append(gen_masks[j][np.newaxis, ...])
                j += 1
            else:
                images.append(source_image[i][np.newaxis])
                masks.append(np.zeros((1, *start_size)))
        return np.concatenate(images, axis=0), np.concatenate(masks, axis=0)

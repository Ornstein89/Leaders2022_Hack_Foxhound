import os

import numpy as np
import pandas as pd
import SimpleITK as sitk
from lungmask import mask as unet_mask
from skimage.transform import resize


def significant_lung_regions(cts, lungs, thresh=0.03):
    """
    selecting normal CT images with (lung area)/(image area) > thresh

    Args:
        Lungs : binary lung masks for normal ct images
        cts : normal ct images
    """
    cts_normal = []
    lungs_normal = []

    for i in range(lungs.shape[0]):
        if np.sum(lungs[i, ...]) / (512 * 512) > thresh:
            cts_normal.append(cts[i, ...])
            lungs_normal.append(lungs[i, ...])

    return np.array(cts_normal), np.array(lungs_normal)


def significant_lung_regions(cts, lungs, thresh=0.03):
    """
    selecting normal CT images with (lung area)/(image area) > thresh

    Args:
        Lungs : binary lung masks for normal ct images
        cts : normal ct images
    """
    cts_normal = []
    lungs_normal = []

    for i in range(lungs.shape[0]):
        if np.sum(lungs[i, ...]) / (512 * 512) > thresh:
            cts_normal.append(cts[i, ...])
            lungs_normal.append(lungs[i, ...])

    return np.array(cts_normal), np.array(lungs_normal)


class SimpleModel:
    """Простая модель.
    Прицип которой заключается в том, что она копирует зоны поражения с
    инфецированного легкого на здоровое.

    Args:
        data_dir_path : str : Путь к папке с данными (ВАЖНО! чтобы в ней была папка COVID19_1110)
        data_path : str : Путь к файлу xlsx в котором хранятся данные о путях к файлам датасета COVID19_1110
        lung_data_path : str : Путь к файлу csv в котором хранятся данные о путях к маскам лёгких для датасета COVID19_1110
    Methods:
        inference(self, input_dicom_path, output_dicomdir_path, infection_idx=None) : Загружает и генерирует новый dicom файл.
    """

    def __init__(self, data_dir_path, data_path, lung_data_path) -> None:
        self.data = self._load_data(data_path, lung_data_path)

        self.data = self.data[~self.data.mask_file.isna()]
        self.data_dir_path = data_dir_path

    def inference(self, input_dicom_path, output_dicomdir_path, infection_idx=None):
        """Загружает и генерирует новый dicom файл.

        Args:
            input_dicom_path : str : путь к входному файлу/директории.
            output_dicomdir_path : str : путь к выходному файлу/директории.
            infection_idx : int : id одного из размеченных файлов, если None тогда выбирает случайно.
        Return:
            synthetic_full : ndarray : Сгенерированное изображения (N, H, W)
            synthetic_mask_full : ndarray : Маска поражений сгенерированного изображения (N, H, W)
        """
        row = self._take_infection(infection_idx)
        covid_dataset = os.path.join(self.data_dir_path, "COVID19_1110")
        # get dataset image
        image_path = os.path.join(covid_dataset, row["study_file"][:-3])
        infection_path = os.path.join(covid_dataset, row["mask_file"][:-3])
        lung_path = os.path.join(covid_dataset, row["lung_mask"])

        # get images
        image = self._load_nii(image_path)
        lung = self._load_nii(lung_path)
        infection_mask = self._load_nii(infection_path)

        # get normal
        normal_image = self._load_dicom(input_dicom_path)
        normal_lung = self._lung_segmenation(normal_image)

        normal_image = sitk.GetArrayFromImage(normal_image)

        if normal_image.shape[1:] != image.shape[1:]:
            normal_image = self._resize(normal_image, image.shape[1:])
            normal_lung = self._resize(normal_lung, image.shape[1:])

        assert (normal_lung > 0).sum() > 0, "Lungs hasn't detected!"

        layers = self._get_masked_layers(infection_mask)

        synthetic, synthetic_mask, layers = self._synthetic_image(
            cts_infected=image,
            lungs_infected=lung,
            infection_mask=infection_mask,
            cts_normal=normal_image,
            lungs_normal=normal_lung,
            layers=layers,
        )

        synthetic_full, synthetic_mask_full = self._recover_synthetic_image(
            normal_image, synthetic, synthetic_mask, layers, normal_lung
        )

        return synthetic_full, synthetic_mask_full

    def _lung_segmenation(self, image):
        """
        Сегментирует лёгкие и возвращает маску с лёгкими разделёнными на части.

        Args:
            image : sitk.Image : Скан лёгких
        Return
            segmentation : ndarray : (N, H, W) маска лёгких.
        """
        model = unet_mask.get_model("unet", "LTRCLobes")
        segmentation = unet_mask.apply(image, model)
        return segmentation

    def _load_data(self, data_path, lung_mask_data_path):
        table = pd.read_excel(data_path)
        table.iloc[:, 2] = table.iloc[:, 2].str[1:]
        table.iloc[:, 3] = table.iloc[:, 3].str[1:]
        extra_table = pd.read_csv(lung_mask_data_path)
        extra_table.study_id += 1
        table = table.set_index("study_id")
        table["lung_mask"] = extra_table.set_index("study_id")["lung_mask"]
        return table

    def _take_infection(self, idx=None):
        idx = idx or np.random.choice(self.data.index)
        return self.data.loc[idx]

    def _load_nii(self, file_path):
        return sitk.GetArrayFromImage(sitk.ReadImage(file_path))

    def _load_dicom(self, file_path):
        reader = sitk.ImageSeriesReader()

        dicom_names = reader.GetGDCMSeriesFileNames(
            "../input/dicom-test/2.000000-5mm-81154"
        )
        reader.SetFileNames(dicom_names)

        image = reader.Execute()
        return image

    def _synthetic_image(
        self,
        cts_infected,
        lungs_infected,
        infection_mask,
        cts_normal,
        lungs_normal,
        layers,
    ):
        """
        cts_infected, lungs_infected : infected ct images and corresponding lung masks
        infection_mask : lesion masks for infected cts
        cts_normal, lungs_normal : normal ct images and corresponding lung masks
        """
        cts_infected = cts_infected[layers]
        lungs_infected = lungs_infected[layers] > 0
        infection_mask = infection_mask[layers]
        cts_normal = cts_normal[layers]
        lungs_normal = lungs_normal[layers] > 0

        cts_normal, lungs_normal = significant_lung_regions(cts_normal, lungs_normal)

        # extracting infection regions
        inf_region = cts_infected * infection_mask

        # inversing infection masks
        y_inv = 1 - infection_mask

        assert cts_normal.shape == inf_region.shape, "Different forms!"

        # inserting infection regions into normal cts
        ct_normal_plus_infection = cts_normal * y_inv + inf_region

        # removing infection regions outside the lung area
        ct_synthetic = ct_normal_plus_infection * lungs_normal

        # generating synthesized masks
        infection_mask_synthetic = infection_mask * lungs_normal

        # Selecting synthetic ct images with infection_rate greater than the threshold
        thresh = 0.01
        original_layers = []
        ct_synthetic_sig = []
        infection_mask_synthetic_sig = []
        for i, layer in zip(range(ct_synthetic.shape[0]), layers):
            infection_rate = np.sum(infection_mask_synthetic[i, ...]) / np.sum(
                lungs_normal[i, ...]
            )
            if infection_rate > thresh:
                original_layers.append(layer)
                ct_synthetic_sig.append(ct_synthetic[i, ...])
                infection_mask_synthetic_sig.append(infection_mask_synthetic[i, ...])
        ct_synthetic_sig = np.array(ct_synthetic_sig)
        infection_mask_synthetic = np.array(infection_mask_synthetic_sig)

        return ct_synthetic_sig, infection_mask_synthetic, np.array(original_layers)

    def _get_masked_layers(self, mask):
        layers = np.arange(mask.shape[0])
        not_empty_layers = layers[~np.all(mask == 0, axis=(1, 2))]
        return not_empty_layers

    def _lung_with_bg(self, image, synthetic, lung_mask):
        return image * (1 - (lung_mask > 0)) + synthetic

    def _resize(self, image, size):
        resized_images = []
        for idx in range(image.shape[0]):
            img = resize(image[idx], size)
            resized_images.append(img[np.newaxis, ...])
        return np.concatenate(resized_images, axis=0)

    def _recover_synthetic_image(
        self, image, synthetic, synthetic_mask, layers, normal_lung
    ):
        images = []
        masks = []
        j = 0
        for i in np.arange(image.shape[0]):
            if i in layers:
                images.append(
                    self._lung_with_bg(image[i], synthetic[j], normal_lung[i])[
                        np.newaxis
                    ]
                )
                masks.append(synthetic_mask[j][np.newaxis])
                j += 1
            else:
                images.append(image[i][np.newaxis])
                masks.append(np.zeros((1, 512, 512)))
        return np.concatenate(images, axis=0), np.concatenate(masks, axis=0)


if __name__ == "__main__":
    # Example
    model = SimpleModel(
        "D:\Projects\Leaders2022_Hack_Foxhound\data",
        "D:\Projects\Leaders2022_Hack_Foxhound\data\COVID19_1110\dataset_registry.xlsx",
        "D:\Projects\Leaders2022_Hack_Foxhound\data\COVID19_1110\lung_data.csv",
    )

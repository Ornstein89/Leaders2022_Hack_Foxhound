import numpy as np
from PIL import Image
import SimpleITK as sitk
from skimage.transform import resize
import cv2

def normalize(x):
    """MinMax normalize"""
    min_in = np.min(x)
    max_in = np.max(x)
    return (x - min_in) / (max_in - min_in + 1e-8)

def unnormalize(image, min_source, max_scource):
    return image*(max_scource - min_source) + min_source

def slice2rgb(image, normalize_data=True):
    """Slice of scan -> RGB Image"""
    image = image.astype(np.float32)
    image = normalize(image) if normalize_data else image
    image *= 255
    image = np.dstack((image, image, image)).astype(np.uint8)
    return Image.fromarray(image)

def mask2blue(mask):
    """Scan mask -> RGB Image (where mask is blue)"""
    zeros = np.zeros_like(mask)
    mask = np.dstack((zeros, zeros, mask * 255)).astype(np.uint8)
    return Image.fromarray(mask)
    
def blend(image, mask, normalize_data=True):
    return Image.blend(
        slice2rgb(image, normalize_data=True),
        mask2blue(mask),
        alpha=.2
    )

def load_dicom(file_path):
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(file_path)
    reader.SetFileNames(dicom_names)

    image = reader.Execute()
    return image

def read_image(path):
    return sitk.GetArrayFromImage(sitk.ReadImage(path))

def image2gray255(image):
    return np.uint8((normalize(image))*255)

def gray2rgb255(gray):
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

def resize_cube(self, image, size):
        resized_images = []
        for idx in range(image.shape[0]):
            img = resize(image[idx], size)
            resized_images.append(img[np.newaxis, ...])
        return np.concatenate(resized_images, axis=0)

def rgb2gray(rgb_image):
    return cv2.cvtColor(rgb_image, cv2.COLOR_RGB2GRAY)
import cv2
import numpy as np
import pydicom
import SimpleITK as sitk
from PIL import Image
from pydicom import dcmread
from skimage.transform import resize

from app.services.file import FileService


def normalize(x):
    """MinMax normalize"""
    min_in = np.min(x)
    max_in = np.max(x)
    return (x - min_in) / (max_in - min_in + 1e-8)


def unnormalize(image, min_source, max_scource):
    return image * (max_scource - min_source) + min_source


def slice2rgb(image, normalize_data=True):
    """Slice of scan -> RGB Image"""
    image = image.astype(np.float32)
    image = normalize(image) if normalize_data else image
    image *= 255
    image = np.dstack((image, image, image)).astype(np.uint8)
    return Image.fromarray(image)


def slice2dicom(image, original_path, normalize_data=True):
    """Slice of scan -> DICOM file"""
    dicom_file = dcmread(original_path)
    image = image.astype(np.float32)
    image = normalize(image) if normalize_data else image
    image *= 255
    image = np.dstack((image, image, image)).astype(np.uint16)
    new_file_name = FileService.generate_file_path()
    newds = pydicom.Dataset()
    newds.file_meta = dicom_file.file_meta

    newds.Rows = image.shape[0]
    newds.Columns = image.shape[1]
    newds.NumberOfFrames = 1

    newds.PixelSpacing = dicom_file.PixelSpacing  # in mm
    newds.SliceThickness = dicom_file.SliceThickness  # in mm

    newds.BitsAllocated = dicom_file.BitsAllocated
    newds.PixelRepresentation = dicom_file.PixelRepresentation
    newds.SamplesPerPixel = dicom_file.SamplesPerPixel
    newds.PhotometricInterpretation = dicom_file.PhotometricInterpretation
    newds.BitsStored = dicom_file.BitsStored
    newds.PixelData = image.tobytes()
    newds.save_as(new_file_name, write_like_original=False)
    return new_file_name


def mask2blue(mask):
    """Scan mask -> RGB Image (where mask is blue)"""
    zeros = np.zeros_like(mask)
    mask = np.dstack((zeros, zeros, mask * 255)).astype(np.uint8)
    return Image.fromarray(mask)


def blend(image, mask, normalize_data=True):
    return Image.blend(
        slice2rgb(image, normalize_data=True), mask2blue(mask), alpha=0.2
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
    return np.uint8((normalize(image)) * 255)


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

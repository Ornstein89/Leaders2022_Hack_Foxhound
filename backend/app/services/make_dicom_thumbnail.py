from typing import Optional

import numpy as np
from PIL.Image import Image, Resampling, fromarray
from pydicom import dcmread
from sklearn.preprocessing import minmax_scale


def make_dicom_thumbnail(filename: str, size: tuple) -> Optional[Image]:
    """
    Сохраняет уменьшенное чёрно-белое изображение для предпросмотра
    из файла формата  DICOM, содержащего чёрно-белое 8- или 16-битное изображение

    Args:
        filename (str): путь к файлу DICOM
        size (tuple): кортеж с размерами создаваемой уменьшенной копии, например (128, 128)

    Returns:
        PIL.Image: изображение в формате объекта  PIL.Image или None, сохраняется в файл
        с помощью метода save("имя_файла")

    Примеры:
        filename = "1-01.dcm"
        display(make_dicom_thumbnail(filename=filename, size=(256, 256)))
        make_dicom_thumbnail(filename=filename, size=(256, 256).save("test_img.png")
    """

    try:
        ds = dcmread(filename)
        orig_shape = ds.pixel_array.shape
        ds.pixel_array[ds.pixel_array < 0] = ds.pixel_array.max()
        normalized_array = minmax_scale(
            ds.pixel_array.flatten(), feature_range=(0, 255)
        )
        uint8_array = normalized_array.reshape(orig_shape).astype(dtype=np.uint8)
        pil_image = fromarray(uint8_array, "L")
        pil_image.thumbnail(size, Resampling.LANCZOS)
        return pil_image
    except Exception:
        return None

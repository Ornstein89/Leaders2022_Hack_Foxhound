import os
import numpy as np
from PIL import Image

def normalize(x):
    """MinMax normalize"""
    min_in = np.min(x)
    max_in = np.max(x)
    return (x - min_in) / (max_in - min_in + 1e-8)

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
import os
import sys
from skimage.filters import gaussian
import matplotlib.pyplot as plt
from skimage import io
from skimage.util import img_as_uint, img_as_float


def gaussianHighPass(image_path: str, sigma):
    image = io.imread(image_path)
    image =img_as_float(image)
    blurred_image = gaussian(image, sigma=sigma, preserve_range=True)
    filtered_image = image - blurred_image
    return filtered_image

def gaussianLowPass(image_path: str, sigma):
    image = io.imread(image_path)
    image =img_as_float(image)
    blurred_image = gaussian(image, sigma=sigma, preserve_range=True)
    return blurred_image

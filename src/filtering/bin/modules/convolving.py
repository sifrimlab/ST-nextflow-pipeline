import os
import sys
from skimage.filters import gaussian
import matplotlib.pyplot as plt
from skimage import io
from skimage.util import img_as_uint


def gaussianPass(image_path: str, sigma):
    image = io.imread(image_path)
    filtered_image = gaussian(image, sigma=sigma)
    return filtered_image

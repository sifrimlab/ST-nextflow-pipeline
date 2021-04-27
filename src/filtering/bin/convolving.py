import os
import sys
from skimage.filters import gaussian
import matplotlib.pyplot as plt
from skimage import io
from skimage.util import img_as_uint


def gaussianPass(image_path: str, sigma):
    image = io.imread(image_path)
    filtered_image = gaussian(image, sigma=3)
    return filtered_image


# input parsing

image_path = sys.argv[1]
prefix = os.path.splitext(image_path)[0]
sigma = sys.argv[2]
filtered_image = gaussianPass(image_path, sigma)
filtered_image = img_as_uint(filtered_image)
io.imsave(f"{prefix}_filtered.tif", filtered_image)

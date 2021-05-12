import numpy as np
import matplotlib.pyplot as plt
from skimage import io
import cv2

def findCutOffPercentile(image_array, percent: int):
    flattened = image_array.flatten()
    flattened = np.sort(flattened)
    cutoff_value = (flattened[int(len(flattened) * percent / 100)])
    return cutoff_value

def cutOffPercentile(image_array, percent: int):
    cutoff_value = findCutOffPercentile(image_array, percent)
    bool_array = np.where(image_array < cutoff_value, 0,image_array)
    float_image = bool_array.astype(float)
    return float_image

def basicNormalize(image_array):
    minimum = np.amin(image_array)
    maximum = np.amax(image_array)
    # Given that minimum will most likely be 0, you're just doing basic dividing by max 
    norm_image = (image_array - minimum) * (1.0 / (maximum - minimum))
    return norm_image

def clipAndNormalize(path_to_image: str, percent_to_clip: int, prefix=""):
    if not 0 <= percent_to_clip <100:
        raise Exception(f"Inputted percentage {percent_to_clip} is not between 0 and 100")
    image = io.imread(path_to_image)
    cut_image = cutOffPercentile(image, percent=percent_to_clip)
    return cut_image
    io.imsave(f"{prefix}_normalized.tif", cut_image)


def basicNormalizeOverMultipleImages(img_path_list):
    img_list = [io.imread(image) in img_path_list]
    minima = [np.amin(img) for img in img_list]
    maxima = [np.amax(img) for img in img_list]



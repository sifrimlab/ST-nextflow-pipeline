import numpy as np
import matplotlib.pyplot as plt
from skimage import io
import cv2
from icecream import ic
image = "/home/david/Documents/image_registration/reference.tif"

image = io.imread(image)

def findCutOffPercentile(image_array, percent: int):
    flattened = image_array.flatten()
    flattened = np.sort(flattened)
    cutoff_value = (flattened[int(len(flattened) * percent / 100)])
    return cutoff_value

def cutOffPercentile(image_array, percent: int):
    cutoff_value = findCutOffPercentile(image, 90)
    bool_array = np.where(image < cutoff_value, 0,image)
    float_image = bool_array.astype(float)
    return float_image

def normalize(image_array):
    minimum = np.amin(image_array)
    maximum = np.amax(image_array)
    # Given that minimum will most likely be 0, you're just doing basic dividing by max 
    norm_image = (image_array - minimum) * (1.0 / (maximum - minimum))
    return norm_image
    
def clipAndNormalize(path_to_image: str, percent_to_clip: int, prefix=""):
    if not (0 <= percent_to_clip <100):
        raise Exception(f"Inputted percentage {percent_to_clip} is not between 0 and 100")
    image = io.imread(image)
    cut_image = cutOffPercentile(image, percent=percent_to_clip)
    io.imsave(f"{prefix}_normalized.tif")


    
    

    
    

    
    

    
    
    




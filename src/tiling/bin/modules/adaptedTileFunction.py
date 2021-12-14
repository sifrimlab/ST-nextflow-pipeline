from skimage.io import imread_collection, imsave, imread
from skimage import io
import numpy as np
from tifffile import imsave
from typing import List
import glob
import os

def calculateOptimalLargestResolution(images: str, target_tile_height: int, target_tile_width: int) -> List[int]: 
    images_array = np.array(io.ImageCollection(images))

    heights = []
    widths = []
    for i in range(len(images_array)):
        heights.append(images_array[i].shape[0])
        widths.append(images_array[i].shape[1])
    max_rows = max(heights) #TODO use buitlin max function
    max_columns = max(widths)

    ydiv = np.ceil(max_rows / target_tile_height)
    xdiv = np.ceil(max_columns / target_tile_width)

    target_full_rows = ydiv * target_tile_height
    target_full_columns = xdiv * target_tile_width

    return int(target_full_rows), int(target_full_columns), int(ydiv), int(xdiv)

def padImage(image_path: str, target_full_rows: int, target_full_columns: int) -> np.ndarray:
    image = imread(image_path)

    rowdiff = target_full_rows - image.shape[0]
    columndiff = target_full_columns - image.shape[1]
    padded_img = np.pad(image, ((0, rowdiff), (0, columndiff)))
    return padded_img

def tileImage(image_path: str, ydiv: int, xdiv: int, image_prefix: str="test"):
    image = imread(image_path)
    temp_split = np.array_split(image, ydiv, axis = 0)
    # Item sublist part is just to unpack a list of lists into one list
    final_split = [item for sublist in [np.array_split(row, xdiv, axis = 1) for row in temp_split] for item in sublist]#TODO what is axis=2?

    for i, img in enumerate(final_split, 1):
        imsave(f"{image_prefix}_tile{i}.tif", img) #TODO explain the better f-string format

def globalfunc(glob_pattern, target_tile_width, target_tile_height):
    target_full_rows, target_full_columns, ydiv, xdiv = calculateOptimalLargestResolution(glob_pattern, 500, 500)
    padded_imgs = {}
    for image_path in glob.glob(glob_pattern):
        padded_imgs[os.path.splitext(os.path.basename(image_path))[0]] = padImage(image_path, int(target_full_rows), int(target_full_columns))

    for k, padded_img in padded_imgs.items():
        tileImage(padded_img, target_tile_height = target_full_rows, target_tile_width = target_full_columns, ydiv = ydiv, xdiv = xdiv, image_prefix = k)
        

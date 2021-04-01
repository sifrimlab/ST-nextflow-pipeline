# importing the module 
import os
import cv2
import sys
import glob
from icecream import ic
from PIL import Image
# important for giant tiff files, otherwise PIL thinks it's malware
Image.MAX_IMAGE_PIXELS = None  

def getResolution(filepath):
    """Prints the resolution of the given image.

    Parameters
    ----------
    filepath : str
        Path to input image.

    Returns
    -------
    int, int
        returns the amount of width and height pixels the input image has: (X,Y)
    """
    im = Image.open(filepath)
    width, height = im.size
    return width, height
    # if x:
    #     return width
    # else:
    #     return height
glob_path="/media/tool/moved_from_m2/cartana_test_stitched/Round*/*" #sys.argv[1]

x__list, y__list = zip(*[getResolution(file) for file in glob.glob(glob_path)])
max_x = max(x__list)
max_y = max(y__list)
print(max_x)
print(max_y)
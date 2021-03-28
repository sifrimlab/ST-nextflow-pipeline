# importing the module 
import os
from PIL import Image
# important for giant tiff files, otherwise PIL thinks it's malware
Image.MAX_IMAGE_PIXELS = None
import cv2
from icecream import ic


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

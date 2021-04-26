from skimage import io
from skimage.feature import blob_log
from skimage import exposure
from skimage.morphology import extrema
import cv2
import os
import sys
import numpy as np

# Beware, not giving min/max sigma's prompts skimage to calculate it, which takes at least twice as long, so for largescale use this is not a good idea
def laplacianOfGaussianBlobDetector(image, min_sigma=None, max_sigma=None):
    """Wrapper for the skimage.feature.blob_log function. Warning: Image gets temporarily converted into 8-bit for improved spot detection

    Parameters
    ----------
    image : nd.array
        Image on which spot detection is to be performed.
    min_sigma : int, optional
        [description], by default None
    max_sigma : int, optional
        [description], by default None
    num_sigma : int, optional
        [description], by default None
    threshold : int, optional
        [description], by default None

    Returns
    -------
    [type]
        [description]
    """
    image = image.astype('uint8')
    if min_sigma is None or max_sigma is None:
        blobs=blob_log(image)
        print("No sigma's received as input for the spot detection. This will increase computation time.")
    else:
        blobs = blob_log(image, min_sigma=int(min_sigma), max_sigma=int(max_sigma))
    return blobs

def localMaximaBlobDetection(image_path: str):
    image = io.imread(image_path)
    local_maxima = extrema.local_maxima(image)



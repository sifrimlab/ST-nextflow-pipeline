from skimage import io
from skimage.feature import blob_log
from skimage import exposure
from skimage.morphology import extrema
import cv2
import os
import sys
import numpy as np
import re
from icecream import ic
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


## Argument parsing:
'''
    python spotDetection.py image_path tile_number min_sigma max_sigma round_number channel_number num_sigma threshold
'''
image = io.imread(sys.argv[1])
prefix = os.path.splitext(sys.argv[1])[0]
tile_number = re.findall(r'tiled_\d+', sys.argv[1])[0].split("_")[1]

if len(sys.argv)>2:
    min_sigma=sys.argv[2]
    max_sigma=sys.argv[3]
else:
    min_sigma=None
    max_sigma=None
if len(sys.argv)>4:
    round_prefix =sys.argv[4] 
    channel_prefix = sys.argv[5]
    round_piece = re.findall(fr'{round_prefix}\d+', prefix)[0]
    channel_piece = re.findall(fr'{channel_prefix}\d+', prefix)[0]
    round_number = re.findall(r'\d+', round_piece)[0]
    channel_number = re.findall(r'\d+', channel_piece)[0]
    round_bool = True
else:
    round_bool = False


array = laplacianOfGaussianBlobDetector(image, min_sigma, max_sigma) # --> returns array: [rows, columns, sigma] = [Y, X, sigma] in image terms
# Insert columns into the array of spots based on the metadata of the input image.
array = np.insert(array, 0, tile_number, axis=1)
if round_bool:
    array = np.insert(array, 1, round_number, axis=1)
    array = np.insert(array, 2, channel_number, axis=1)
array = array.astype(int)

if not round_bool:
    np.savetxt(f"{prefix}_blobs.csv", array, delimiter=',',fmt='%i', header='Tile,Y,X,Sigma',comments='')
else:
    np.savetxt(f"{prefix}_hybs.csv", array,delimiter=',',fmt='%i', header='Tile,Round,Channel,Y,X,Sigma',comments='')


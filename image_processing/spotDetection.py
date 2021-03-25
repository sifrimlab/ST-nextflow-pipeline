from skimage import io
from skimage.feature import blob_log
from skimage import exposure
import cv2
import os
import sys
import numpy as np
import re
# Beware, not giving min/max sigma's prompts skimage to calculate it, which takes at least twice as long, so for largescale use this is not a good idea
def laplacianOfGaussianBlobDetector(image, min_sigma=None, max_sigma=None):
    if min_sigma is None or max_sigma is None:
        blobs=blob_log(image)
        print("No sigma's received as input for the spot detection. This will increase computation time.")
    else: 
        blobs = blob_log(image, min_sigma, max_sigma)
    return blobs


image = io.imread(sys.argv[1])
prefix = os.path.splitext(sys.argv[1])[0]
tile_number = re.findall(r'\d+', sys.argv[2])[0]


if len(sys.argv)>3:
    min_sigma=sys.argv[3]
    max_sigma=sys.argv[4]
else:
    min_sigma=None
    max_sigma=None

if len(sys.argv)>5:
    round_bool = True
    round_number = re.findall(r'\d+', sys.argv[5])[0]
    channel_number = re.findall(r'\d+', sys.argv[6])[0]
else:
    round_bool = False

# image = exposure.equalize_hist(image)
array = laplacianOfGaussianBlobDetector(image, min_sigma, max_sigma)
array = np.insert(array, 0, tile_number, axis=1)
if round_bool:
    array = np.insert(array, 1, round_number, axis=1)
    array = np.insert(array, 2, channel_number, axis=1)
array = array.astype(int)

if not round_bool:
    np.savetxt(f"{prefix}_blobs.csv", array, delimiter=',',fmt='%i', header='Tile,X,Y,Sigma',comments='')
else:
    np.savetxt(f"{prefix}_hybs.csv", array,delimiter=',',fmt='%i', header='Tile,Round,Channel,X,Y,Sigma',comments='' )


from skimage import io
import os
import sys
import numpy as np
import re
from modules.spotDetection import laplacianOfGaussianBlobDetector

## Argument parsing:
'''
    python spotDetection.py image_path tile_number min_sigma max_sigma round_number channel_number num_sigma threshold
'''
image = io.imread(sys.argv[1])
prefix = os.path.splitext(sys.argv[1])[0]
tile_number =re.findall(r'\d+', re.findall(r'tile\d+', sys.argv[1])[0])[0]

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


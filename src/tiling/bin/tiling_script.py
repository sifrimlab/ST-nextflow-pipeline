import cv2
import math
import sys
import os
from skimage import io
from modules.tilingHelperFunctions import calculateOptimalTileSize, writeTiles


image = sys.argv[1]
prefix = os.path.splitext(image)[0]
tile_x, tile_y = calculateOptimalTileSize(image,sys.argv[2], sys.argv[3])
writeTiles(image, prefix, tile_size_x=tile_x, tile_size_y=tile_y)
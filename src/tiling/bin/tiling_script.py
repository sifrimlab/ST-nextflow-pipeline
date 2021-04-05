import sys
import os
from modules.tilingHelperFunctions import writeTiles


image = sys.argv[1]
prefix = os.path.splitext(image)[0]
tile_x, tile_y = int(sys.argv[2]), int(sys.argv[3])
writeTiles(image, prefix, tile_size_x=tile_x, tile_size_y=tile_y)
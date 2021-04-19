import re
import os
import sys
from skimage import io
from modules.stitch import stitchImageList

tile_grid_size_x = int(sys.argv[1])
tile_grid_size_y = int(sys.argv[2])
tile_grid_size = (tile_grid_size_x,tile_grid_size_y)
tile_size_x = int(sys.argv[3])
tile_size_y = int(sys.argv[4])
image_path_list = [sys.argv[i] for i in range(5, len(sys.argv))] # In almost all cases, this will be just a bunch of tiled images from the same origin
raw_prefix = os.path.splitext(image_path_list[0])[0]
# remove the tiled part of the prefix, because we're combining all tiles into one stitched image
prefix = re.sub(r"_tiled_\d+", "", raw_prefix)
stitched_image = stitchImageList(image_path_list, tile_grid_size, tile_size_x, tile_size_y)
io.imsave(f"{prefix}_stitched.tif", stitched_image)


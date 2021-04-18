import numpy as np
import sys
from matplotlib import pyplot as plt
from modules.stitch import stitchImageList


tile_grid_size = sys.argv[1]
tile_size_x = sys.argv[2]
tile_size_y = sys.argv[3]
image_path_list = [sys.argv[i] for i in range(4, len(sys.argv))]
stitched_image = stitchImageList(image_path_list, tile_grid_size, tile_size_x, tile_size_y)
plt.imshow(stitched_image)
plt.show()

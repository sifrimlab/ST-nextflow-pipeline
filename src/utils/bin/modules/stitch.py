import numpy as np
from matplotlib import pyplot as plt
import re
import cv2

image_path_list = [f"/media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/results/tiled_ref/REF_padded_tiled_{i}.tif" for i in range(1,5)]
# image_list = [cv2.imread(image, -1) for image in image_path_list]
tile_image_dict = {re.findall(r"tiled_\d+", image_path)[0]: image_path for image_path in image_path_list}

tile_grid = (2,2)




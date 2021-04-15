import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import colorConverter
import pandas as pd
import cv2
import sys
from ast import literal_eval as make_tuple
from modules.imageViewing import plotDecodedGenesOnWholeImage

reference_image = sys.argv[1]
decoded_genes = sys.argv[2]
tile_grid_shape = make_tuple(sys.argv[3])
tile_size_x = int(float(sys.argv[4]))
tile_size_y = int(float(sys.argv[5]))
plotDecodedGenesOnWholeImage(reference_image, decoded_genes, tile_grid_shape, tile_size_x, tile_size_y)
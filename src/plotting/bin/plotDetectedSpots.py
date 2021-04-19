import sys
from ast import literal_eval as make_tuple
from modules.imageViewing import plotSpotsOnWholeImage

detected_spots = sys.argv[1]
tile_grid_shape = make_tuple(sys.argv[2])
tile_size_x = int(float(sys.argv[3]))
tile_size_y = int(float(sys.argv[4]))
plotSpotsOnWholeImage(detected_spots, tile_grid_shape, tile_size_x, tile_size_y)


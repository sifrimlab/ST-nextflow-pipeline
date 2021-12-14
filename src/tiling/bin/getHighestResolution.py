# importing the module 
import os
import sys
from modules.adaptedTileFunction import calculateOptimalLargestResolution


target_tile_x = int(sys.argv[1])
target_tile_y = int(sys.argv[2])
glob_path= [sys.argv[i] for i in range(3, len(sys.argv))]


max_y, max_x, ydiv, xdiv = calculateOptimalLargestResolution(images = glob_path, target_tile_height = target_tile_y, target_tile_width = target_tile_x) 
print(max_x)
print(max_y)
print(xdiv)
print(ydiv)

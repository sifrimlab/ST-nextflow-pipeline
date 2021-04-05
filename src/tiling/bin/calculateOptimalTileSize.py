from modules.tilingHelperFunctions import calculateOptimalTileSize
import sys

# Argparsing
max_x, max_y = int(sys.argv[1]), int(sys.argv[2])
target_X, target_Y = int(sys.argv[3]), int(sys.argv[4])

#function calling to calc tile size
tile_size_x, tile_size_y, grid_size_x, grid_size_y = calculateOptimalTileSize(max_x, max_y, target_X, target_Y)
print(tile_size_x)
print(tile_size_y)
print(grid_size_x)
print(grid_size_y)
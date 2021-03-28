from tiling import calculateOptimalTileSize
import sys

# Argparsing
img_path = sys.argv[1]
target_X, target_Y = int(sys.argv[2]), int(sys.argv[3])

#function calling to calc tile size
tile_size_x, tile_size_y = calculateOptimalTileSize(img_path, target_X, target_Y)
# print(f"{tile_size_x} {tile_size_y}")
print(tile_size_x)
print(tile_size_y)
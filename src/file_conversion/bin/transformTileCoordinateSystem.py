import os
import sys
import pandas
from modules.transformTileCoordinateSystem import transformTileCoordinateSystem

csv_file = sys.argv[1]
prefix = os.path.splitext(csv_file)[0]
tile_grid_shape = (int(sys.argv[2]),int(sys.argv[3]))
tile_size_x = int(sys.argv[4])
tile_size_y = int(sys.argv[5])
csv_df = transformTileCoordinateSystem(csv_file, tile_grid_shape, tile_size_x, tile_size_y)
csv_df.to_csv(f"{prefix}_transformed.csv", index=False)




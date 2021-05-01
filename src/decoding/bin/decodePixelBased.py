import sys
import csv
import re
from modules.pixelBasedDecoding import decodePixelBased

# Input parsing:

x_dim = int(sys.argv[1])
y_dim = int(sys.argv[2])
tile_nr =  sys.argv[3]
tile_nr_int = int(re.findall(r"\d+", tile_nr)[0])
codebook = sys.argv[4]
bit_len =  int(sys.argv[5])
threshold = float(sys.argv[6])
image_path_list = [sys.argv[i] for i in range(7, len(sys.argv))]
decoded_df = decodePixelBased(x_dim,y_dim, codebook, bit_len, image_path_list, threshold)
decoded_df['Tile'] = [tile_nr_int for i in range(0,len(decoded_df))]
decoded_df.to_csv(f"decoded_{tile_nr}.csv", index=False)

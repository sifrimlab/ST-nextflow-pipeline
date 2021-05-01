import sys
import csv
import re
from modules.pixelBasedDecoding import decodePixelBased

# Input parsing:

x_dim = int(sys.argv[1])
y_dim = int(sys.argv[2])
tile_nr =  sys.argv[3]
codebook = sys.argv[4]
bit_len =  int(sys.argv[5])
threshold = float(sys.argv[6])
image_path_list = [sys.argv[i] for i in range(7, len(sys.argv))]
decodePixelBased(x_dim,y_dim, codebook, bit_len, image_path_list, threshold).to_csv(f"decoded_{tile_nr}.csv", index=False)

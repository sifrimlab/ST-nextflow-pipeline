import sys
import csv
import re
from modules.decoding import decodeSequentialMaxIntensity

# Input parsing:
intensities = sys.argv[1]
codebook = sys.argv[2]
tile_nr = re.findall(r'\d+', sys.argv[1])[0]

decodeSequentialMaxIntensity(intensities, codebook, tile_nr).to_csv(f"decoded_tiled_{tile_nr}.csv")

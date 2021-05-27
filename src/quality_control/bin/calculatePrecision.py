import sys
import os
import re
import json
from modules.spotDetectionQC import checkSpotsInRoundPrecision

tile_nr_prefix = sys.argv[1]
tile_nr =int(re.findall(r"\d+", tile_nr_prefix)[0])

round_nr_prefix = sys.argv[2]
round_nr =int(re.findall(r"\d+", round_nr_prefix)[0])

pixel_distance =int(sys.argv[3])

ref_spots_csv = sys.argv[4]
round_csv_list = [sys.argv[i] for i in range(5, len(sys.argv))]

# If no spot are found, it will try to unpack null, which needs to be excepted
# and then the function needs to exit, since without spots on a certain round, no complete barcode will be found
try:
    closest_ref_point_dict, attribute_dict = checkSpotsInRoundPrecision(ref_spots_csv, round_csv_list, round_nr, pixel_distance=pixel_distance, x_column_name="X", y_column_name="Y")
except TypeError:
    # So in that case, create a new dict that'll just be empty dicts, to be handled when creating the HTML report
    closest_ref_point_dict = {}
    attribute_dict = {}

with open(f"{tile_nr_prefix}_{round_nr_prefix}_closest_ref_point_dict.json", "a+") as jsonfile:
    json.dump(closest_ref_point_dict, jsonfile)
with open(f"{tile_nr_prefix}_{round_nr_prefix}_precision_stats.json", "a+") as jsonfile:
    json.dump(attribute_dict, jsonfile)



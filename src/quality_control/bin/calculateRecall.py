import sys
import os
import re
import json
from modules.spotDetectionQC import calculateRecall

tile_nr_prefix = sys.argv[1]
tile_nr =int(re.findall(r"\d+", tile_nr_prefix)[0])

ref_spots_csv = sys.argv[2]
closest_ref_point_dicts_list = [sys.argv[i] for i in range(3, len(sys.argv))]

dict_of_closest_ref_point_dicts = {} # key = round_nr, value = a closest_ref_dict for that tile/round combination
for json_path in closest_ref_point_dicts_list:
    with open(json_path, 'r') as json_file:
        round_nr  = int(re.findall(r"\d+", re.findall(r"Round\d+", json_path)[0])[0])
        data = json.load(json_file)
        dict_of_closest_ref_point_dicts[round_nr] = data

attribute_dict, round_not_found, plot = calculateRecall(ref_spots_csv, dict_of_closest_ref_point_dicts)

with open(f"{tile_nr_prefix}_recall_stats.json", "a+") as jsonfile:
    json.dump(attribute_dict, jsonfile)

with open(f"{tile_nr_prefix}_round_not_found.json", "a+") as jsonfile:
    json.dump(round_not_found, jsonfile)

plot.savefig(f"{tile_nr_prefix}_recall_per_round.png")





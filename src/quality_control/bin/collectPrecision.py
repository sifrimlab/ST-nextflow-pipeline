import sys
import json
import re

# This should be mapped per round
round_nr_prefix = sys.argv[1]
# round_nr_prefix="Round1"
round_nr = int(re.findall(r"\d+", round_nr_prefix)[0])


attribute_jsons_list = [sys.argv[i] for i in range(2, len(sys.argv))]
# attribute_jsons_list = [f"/media/nacho/Puzzles/gabriele_data/1442_OB/results_correct_codebook_whiteDisk3_minSigma2_maxSigma20_noNorm_stardistSegmentation_voronoiAssigned_spotDetectionQC/quality_control/spot_detection_QC/precision/tiled_{i}_Round1_precision_stats.json" for i in range(1, 5)]

total_attributes_dict = {} # represents one row
for json_path in attribute_jsons_list:
    with open(json_path, 'r') as json_file:
        # round_nr  = int(re.findall(r"\d+", re.findall(r"Round\d+", json_path)[0])[0])
        data = json.load(json_file)
        print(data)
        for attribute, value in data.items():
            total_attributes_dict[attribute] = total_attributes_dict.get(attribute, 0) + value
# Watch out, just incrementing values will not always be logical, for instance when cumulating ratio's, or the round number, so we hard-adapt that, will probably result in keyErrors down the line
total_attributes_dict["Round #"]= round_nr

try:
    total_attributes_dict["Ratio of matched spots"] = round(total_attributes_dict['# matched spots'] / total_attributes_dict["Total Spots"], 3) * 100
except:
    total_attributes_dict["Ratio of matched spots"] = 0

with open(f"{round_nr_prefix}_total_attributes.json", "a+") as jsonfile:
    json.dump(total_attributes_dict, jsonfile)


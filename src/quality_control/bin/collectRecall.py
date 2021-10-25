import sys
import json
import re
import matplotlib.pyplot as plt


recall_stats_json_list = []
round_not_found_list = []

#argparsing, because 2 lists of files will be input, they will vary in size depending on the number of tiles, so no indexing available
for argument in sys.argv:
    if "recall_stats" in argument:
        recall_stats_json_list.append(argument)
    elif "round_not_found" in argument:
        round_not_found_list.append(argument)

# First we combine the recalls into one line
total_attributes_dict = {} # represents one row
for json_path in recall_stats_json_list:
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
        for attribute, value in data.items():
            total_attributes_dict[attribute] = total_attributes_dict.get(attribute, 0) + value
# Watch out, just incrementing values will not always be logical, for instance when cumulating ratio's, or the round number, so we hard-adapt that, will probably result in keyErrors down the line
total_spots_on_ref = total_attributes_dict["spots on ref"] # assign this to a variable cause we'll need it for the plot below
try:
    total_attributes_dict["Ratio Complete Barcodes"] = round(total_attributes_dict['Complete barcodes'] / total_attributes_dict["spots on ref"], 3) * 100
except:
    total_attributes_dict["Ratio Complete Barcodes"] = 0

with open(f"total_recall_stats.json", "a+") as jsonfile:
    json.dump(total_attributes_dict, jsonfile)


# Then we create the giant "in which round dropped the number of complete barcodes" plot from the round not found list
total_round_not_found = {}
for json_path in round_not_found_list:
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
        for round_nr, value in data.items():
            total_round_not_found[round_nr] = total_attributes_dict.get(round_nr, 0) + value

# Now we make a plot out of at which round  the complete barcode stops
lists = sorted(total_round_not_found.items()) # sorted by key, return a list of tuples
#unzip the list of tuples into x and y
lists = [[ i for i, j in lists ],
      [ j for i, j in lists ]]
x = lists[0]
x_labels = [f"Round {int(i)}" for i in x]

y = lists[1]

# parse y into being a a negatice cumcount, not just absolute values
spots_left = total_spots_on_ref
for i, y_el in enumerate(y):
    spots_left = spots_left - y_el
    y[i] = spots_left

_, ax = plt.subplots(1,1)
ax.bar(x,y, color="maroon")
for rect in ax.patches:
    height = rect.get_height()
    ax.annotate(f'{int(height)}', xy=(rect.get_x()+rect.get_width()/2, height),
                xytext=(0, 5), textcoords='offset points', ha='center', va='bottom')
ax.plot(x,y, "o-k")
ax.set_title(f"Potential complete barcodes left out of the {total_spots_on_ref} spots after each round")
ax.set_ylabel("Number of potential complete barcodes remaining")
ax.set_xticks(x)
ax.set_xticklabels(x_labels, rotation= 45)

plt.savefig("total_drop_complete_barcodes_per_round.svg", dpi=600)



import pandas as pd
from skimage import io
from csv import writer
import sys
import os
import re
## The idea here is to create a new csv that has positions for the round/channel intensities to go, and to update that csv every time a new image is inputted
#input example: [tiled_4, Round3, c2, /home/nacho/Documents/Code/communISS/work/b0/ca1a59e73e0fbcee5b7290a8185dcc/Round3_c2_registered_tiled_4_filtered_registered.tif]
# reference = io.imread("/home/nacho/Documents/Code/communISS/results/filtered_ref/REF_tiled_1_filtered.tif")

# Argument parsing
blobs = pd.read_csv(sys.argv[1])
input_image = io.imread(sys.argv[2])
prefix = os.path.splitext(sys.argv[2])[0]
input_tile = int(re.findall(r'\d+', sys.argv[3])[0])
input_round = int(re.findall(r'\d+', sys.argv[4])[0])
input_channel= int(re.findall(r'\d+', sys.argv[5])[0])
print(prefix)
headers = ["Tile", "Round", "Channel", "Y", "X", "Intensity"]
with open(f"{prefix}_intensities.csv", 'a+', newline='') as write_obj:
    csv_writer = writer(write_obj)
    csv_writer.writerow(headers)
    for blob in blobs[blobs['Tile']==input_tile].itertuples():
        # Skimage slicing works with rows/columns, so x and y need to be changed
        input_intensity = input_image[blob.Y, blob.X]
        row_contents = [input_tile, input_round, input_channel, blob.Y, blob.X, input_intensity]
        csv_writer.writerow(row_contents)

    
    



import pandas as pd
import numpy as np
from skimage import io
from csv import writer
import os
## The idea here is to create a new csv that has positions for the round/channel intensities to go, and to update that csv every time a new image is inputted
#input example: [tiled_4, Round3, c2, /home/nacho/Documents/Code/communISS/work/b0/ca1a59e73e0fbcee5b7290a8185dcc/Round3_c2_registered_tiled_4_filtered_registered.tif]
# reference = io.imread("/home/nacho/Documents/Code/communISS/results/filtered_ref/REF_tiled_1_filtered.tif")




#blobs will be inputted via nextflow
blobs = pd.read_csv("/home/nacho/Documents/Code/communISS/results/blobs/concat_blobs.csv")
headers = ["Tile", "Round", "Channel", "Y", "X", "Intensity"]
input_tile = 4
input_round = 3
input_channel= 2
input_image = io.imread("/home/nacho/Documents/Code/communISS/work/b0/ca1a59e73e0fbcee5b7290a8185dcc/Round3_c2_registered_tiled_4_filtered_registered.tif")
file_exists = os.path.isfile("intensities.csv")


with open("intensities.csv", 'a+', newline='') as write_obj:
    csv_writer = writer(write_obj)
    if not file_exists:
        csv_writer.writerow(headers)
    
    for blob in blobs[blobs['Tile']==input_tile].itertuples():
        # Skimage slicing works with rows/columns, so x and y need to be changed
        input_intensity = input_image[blob.Y, blob.X]
        row_contents = [input_tile, input_round, input_channel, blob.Y, blob.X, input_intensity]
        csv_writer.writerow(row_contents)

    
    



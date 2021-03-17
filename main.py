__author__      = "David Wouters"
__maintainer__ = "David Wouters"
__email__ = "david.wouters1@student.kuleuven.be"
__status__ = "Production"

'''
    Welcome to the starting point of the ISS pipeline. This pipeline is designed to be completely modular and adaptable to your specific usecase,
    However, if you would like to just run a pipeline where you don't have to make any decisions or understand what it's doing, then the default settings will be just fine.
    Be warned that this may cause incredibly boring and unsatisfying results.
    
    Below you will find a set of requirements you have to make sure your data fulfills before running the default pipeline:

    1) The layout of your ISS directory should follow this scheme:
        For now your dirs and files need to be named correctly, however I might build smarter parsing possibilities

    MASTER
    |
    |_______Auxillary_images
    |           |____REF.TIFF
    |           |____DAPI.TIFF
    |
    |________Round1
        |       |____channel1.TIFF
        |       |____channel2.TIFF
        |       |____channel3.TIFF
        |       |____channel4.TIFF
        |
        |____Round2
        |       |____channel1.TIFF
        |       |____channel2.TIFF
        |       |____channel3.TIFF
        |       |____channel4.TIFF
        |
        |____RoundN
        |       |____channel1.TIFF
        |       |____channel2.TIFF
        |       |____channel3.TIFF
        |       |____channel4.TIFF
        ....
    
    2)  Locate your decoding scheme: you're going to need it. Fill it in in the "codebook" variable, or use it as a parameter when this script is called, depending on how you run this pipeline
        It should be a csv file that is built up as such: (with or without header, that doesn't matter)

        Gene, Code
        BRCA2, 124354


'''
## Imports
# pypi
import argparse
import os
import pandas as pd
from skimage.morphology import white_tophat
from icecream import ic
import cv2
import glob

# communISS
from inputParsing import addBackslash, formatISSImages, parseCodebook, formatTiledISSImages, makeDir, addDirIntoPath

from image_processing.normalization.normalization import numpyNormalization
from image_processing.registration.registration_simpleITK import calculateRigidTransform, writeRigidTransformed
from image_processing.filtering import writeFilteredImages
from image_processing.tiling import calculateOptimalTileSize, writeTiles
from decorators import measureTime

# Variables that are needed in multiples places:
tif_suffixes = ("TIFF","TIF")
seperate_aux_images = False
write_intermediate = True
#############################
## Test parameters:
## input_dir = /media/tool/starfish_test_data/ExampleInSituSequencing
## Codebook = /media/tool/starfish_test_data/ExampleInSituSequencing/codebook.csv
## Codebook = /media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/codebook.csv
## command to run: python main.py /media/tool/starfish_test_data/ExampleInSituSequencing /media/tool/starfish_test_data/communISS_output /media/tool/starfish_test_data/ExampleInSituSequencing/codebook.csv
##############################

if __name__ == '__main__':
    # code the argparser for commandline utility
    parser = argparse.ArgumentParser(prog='communISH', description='Run a rudimentary ISS pipeline')
    # input dir for images
    parser.add_argument('input_dir_arg',help='Path to your input directory')
    #output dir for images
    parser.add_argument('output_dir_arg',help='Path to your output directory')
    # input path for codebook
    parser.add_argument('codebook', help='Path to your codebook')
    # flag to see if the user wants to customize or not
    parser.add_argument('--default',action='store_true', help='Flag to indicate whether to run the default pipeline')
    args = parser.parse_args()

    # Parsing the actual arguments.
    # Rest of the pipeline works with absolute paths behind the scenes for the images to avoid any mistakes.
    input_dir = os.path.abspath(args.input_dir_arg) + "/"
    output_dir = os.path.abspath(args.output_dir_arg) + "/"
    codebook_path = os.path.abspath(args.codebook)
    # raise errors if the input files don't exist.
    if not os.path.isdir(input_dir):
        raise ValueError("Inputted directory is not a directory or does not exists")
    if not os.path.isfile(codebook_path):
        raise ValueError("Inputted codebook file does not exist")
    
    # Create output dir
    makeDir(output_dir)

    # Parse detected input images into pandas dataframe.
    image_df = formatISSImages(input_dir=input_dir, silent=True, seperate_aux_files_per_round=seperate_aux_images)
    # Write df to csv for self-check purposes.
    image_df.to_csv("images.csv")

    # Parse codebook
    codebook_dict = parseCodebook(codebook_path)
    
    # Normalize images

    # Calculate registration transformation step 1
    # First create transform dir if it doesn't exist yet
    transform_dir = os.path.join(output_dir, "transforms") + "/"
    makeDir(transform_dir)
    

    # Calculate registration per row
    for row in image_df.itertuples():
        calculateRigidTransform(row.Image_path, row.Reference, row.Round, row.Channel, transform_dir)
        
    # # Create registration dir if it doesn't exist already
    registered_dir = os.path.join(output_dir, "registered") + "/"
    makeDir(registered_dir)
    # Actually warp the images using the transforms
    for row in image_df.itertuples():
        # Format filenames correctly
        transform_file = f"{transform_dir}transform_r{row.Round}_c{row.Channel}.txt"
        registered_file = f"{registered_dir}r{row.Round}_c{row.Channel}_registered.tiff"
        # Actually register the images
        writeRigidTransformed(row.Image_path, transform_file, registered_file)
    
    # Create tile directories
    tiled_dir = os.path.join(output_dir, "tiled") + "/"
    makeDir(tiled_dir)

    ## Tiling the images
    # Iterate over every row, meaning go over every tif image
    for row in image_df.itertuples(): 
        # Get round number of the current iteration
        round_number= row.Round

        # Define the dir path
        round_dir = f"{tiled_dir}Round{round_number}/"
        # Create a dir for it if it doesn't exist already
        makeDir(round_dir)

        # Define channel number of current iteration
        channel_number=row.Channel

        # Calculate the optimal size to get the image to a certain resolution (to be filled in by user. #TODO need to create an argument for this)
        tile_x_size, tile_y_size = calculateOptimalTileSize(row.Image_path, 500,500)

        # Tile the current image
        writeTiles(row.Image_path, tile_x_size, tile_y_size, f"{round_dir}Round{round_number}_Channel{channel_number}")
        # Then also tile its aux images if not done so already for this round
        if not glob.glob(f"{round_dir}Round{round_number}_REF_Tile*"):
            writeTiles(row.Reference, tile_x_size, tile_y_size, f"{round_dir}Round{round_number}_REF")
        if not glob.glob(f"{round_dir}Round{round_number}_DAPI_Tile*"):
            writeTiles(row.DAPI, tile_x_size, tile_y_size, f"{round_dir}Round{round_number}_DAPI")

    # Create a new dataframe to represent the tile images.
    tiled_df = formatTiledISSImages(tiled_dir)
    tiled_df.to_csv("tiled_images.csv")

    # Filtering: (white tophat)
    if write_intermediate:
        filtered_dir = os.path.join(tiled_dir, "filtered") + "/"
        makeDir(filtered_dir)
        writeFilteredImages(tiled_df, filtered_dir)
        
        # Update the dataframe with the new "current working images"
        for col in ('Image_path', 'Reference', 'DAPI'):
            tiled_df[col] = tiled_df[col].apply(addDirIntoPath, args=("filtered","tiled"))
    tiled_df.to_csv("tiled_filtered.csv")
    # Registrataion step 2
    # Make dir if it doesn't exist already
    if write_intermediate:
        registered2_dir = os.path.join(filtered_dir, "registered2") + "/"
        makeDir(registered2_dir)

        #update the dataframe

    


    # spot detection/decoding
    # Visualization

    







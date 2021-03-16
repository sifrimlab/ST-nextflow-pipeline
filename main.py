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
# Imports
# pypi
import argparse
import os
import pandas as pd
from icecream import ic

# communISS
from inputParsing import addBackslash, formatISSImages, parseCodebook

from image_processing.normalization.normalization import numpyNormalization
from image_processing.registration.registration_simpleITK import calculateRigidTransform, writeRigidTransformed
from image_processing.tiling import calculateOptimalTileSize, writeTiles
from decorators import measureTime

# Variables that are needed in multiples places:
tif_suffixes = ("TIFF","TIF")
seperate_aux_images = False
#############################
## Test parameters:
## input_dir = /media/tool/starfish_test_data/ExampleInSituSequencing
## Codebook = /media/tool/starfish_test_data/ExampleInSituSequencing/codebook.csv
## Codebook = /media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/codebook.csv
## command to run: python main.py /media/tool/starfish_test_data/ExampleInSituSequencing /media/tool/starfish_test_data/ExampleInSituSequencing/codebook.csv
##############################

if __name__ == '__main__':
    # code the argparser for commandline utility
    parser = argparse.ArgumentParser(prog='communISH', description='Run a rudimentary ISS pipeline')
    # input dir for images
    parser.add_argument('input_dir',help='Path to your input directory')
    # input path for codebook
    parser.add_argument('codebook', help='Path to your codebook')
    # flag to see if the user wants to customize or not
    parser.add_argument('--default',action='store_true', help='Flag to indicate whether to run the default pipeline')
    args = parser.parse_args()

    # Parsing the actual arguments.
    # Rest of the pipeline works with absolute paths behind the scenes for the images to avoid any mistakes.
    input_dir = addBackslash(os.path.abspath(args.input_dir))
    codebook_path = os.path.abspath(args.codebook)
    if not os.path.isdir(input_dir):
        raise ValueError("Inputted directory is not a directory or does not exists")
    if not os.path.isfile(codebook_path):
        raise ValueError("Inputted codebook file does not exist")
    
    # creating output dir
    output_dir = f"{input_dir}communISS_output/"
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    # parse input images into pandas
    image_df = formatISSImages(input_dir=input_dir, silent=False)
    image_df.to_csv("images.csv")

    # parse codebook
    codebook_dict = parseCodebook(codebook_path)
    
    # Normalize images

    # Calculate registration transformation step 1
    # First create transform dir if it doesn't exist yet
    if not os.path.isdir(f"{output_dir}transforms/"):
        os.mkdir(f"{output_dir}transforms/")
    transform_dir = f"{output_dir}transforms/"

    # calculate registration per row
    for index, row in image_df.iterrows():
        calculateRigidTransform(row["Image_path"], row["Reference"], row["Round"], row["Channel"], transform_dir)
        
    # # create registration dir if it doesn't exist already
    if not os.path.isdir(f"{output_dir}registered/"):
        os.mkdir(f"{output_dir}registered/")
    registered_dir = f"{output_dir}registered/"

    # #actually warp the images using the transforms
    for index, row in image_df.iterrows():
        transform_file = f"{transform_dir}transform_r{row['Round']}_c{row['Channel']}.txt"
        registered_file = f"{registered_dir}r{row['Round']}_c{row['Channel']}_registered.tiff"
        writeRigidTransformed(row['Image_path'], transform_file, registered_file)
    
    # Create tile directories
    if not os.path.isdir(f"{output_dir}tiled/"):
        os.mkdir(f"{output_dir}tiled/")
    tiled_dir = f"{output_dir}tiled/"

    # if not os.path.isdir(f"{tiled_dir}aux_images/"):
    #     os.mkdir(f"{tiled_dir}aux_images/")
    # aux_dir = f"{tiled_dir}aux_images/"

    # Tile the images and create a new dataframe to represent them
    for index, row in image_df.iterrows(): 
        round_number= row['Round']
        if not os.path.isdir(f"{tiled_dir}Round{round_number}/"):
            os.mkdir(f"{tiled_dir}Round{round_number}/")
        round_dir = f"{tiled_dir}Round{round_number}/"

        channel_number=row['Channel']

        # Don't forget to fill in the wanted tile resolution here
        tile_x_size, tile_y_size = calculateOptimalTileSize(row['Image_path'], 500,500)

        # Tile round images
        writeTiles(row['Image_path'], tile_x_size, tile_y_size, f"{round_dir}c{channel_number}")
        # Write aux images in the same dir
        writeTiles(row['Reference'], tile_x_size, tile_y_size, f"{round_dir}REF_Round{round_number}")
        writeTiles(row['DAPI'], tile_x_size, tile_y_size, f"{round_dir}DAPI_Round{round_number}")
    
    
    # Tile the aux images
    
    # registrataion step 2
    # spot detection/decoding
    # Visualization

    







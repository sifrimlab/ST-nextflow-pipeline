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
import argparse
import os
import glob
import pandas as pd
import warnings
import re
from icecream import ic

# variables that are needed in multiples places:
tif_suffixes = ("TIFF","TIF")
## helper functions:
def parseCodebook():
    pass

def formatImages(input_dir):
    '''
        This function takes the input_dir that contains the ISS data.
        It first prints out a layout of the detected tif files for debugging purposes/self control.
        Then it converts the detected hierarchy into a pandas dataframe that stores the absolute path to images from each round/channel combination. 
        The function thus returns this dataframe
    '''
    # first print the file hierarchy
    # print('''Detected tif images are: {}
    # If there are files in here that are not supposed to be taken into account for the analysis, we suggest removing them from the input directory'''.format(listFileHierarchy(input_dir)))

    
    # initialize dataframe
    df = pd.DataFrame(columns=['Round', 'Channel', 'Image_path', 'Reference','DAPI' ])

    # suffix definitions so that recognizing the correct directories is more error robust
    aux_dir_names = ("DO", "AUX_IMAGES", "AUXILLARY_IMAGES")
    round_suffixes = ("ROUND", "R")
    channel_suffixes = ("CHANNEL", "C")
    # loop over directory
    for root, dirs, files in os.walk(input_dir):
        # Isolate the current directory in the walk
        root_base = (root.split("/"))[-1]
        # First check if the auxillary images are found
        if (any(i in root_base.upper() for i in aux_dir_names)):
            try:
                # check if ref is found
                reference = [f for f in files if "REF" in f.upper()][0]
                reference_full = f"{root}/{reference}"
            except:
                reference_full=""
                print("No reference image found!")
            try: 
                # check if dapi is found, after this continue to next iteration because finding round images in the aux dir, because later on I'll give a warning if the ref column is empty.
                dapi = [f for f in files if "DAPI" in f.upper()][0]
                dapi_full = f"{root}/{dapi}"
                continue
            except:
                dapi_full=""
                print("No dapi image found!")
                continue
        
        # If it reaches here, it needs to search for round dirs instead
        if (any(i in root_base.upper() for i in round_suffixes)):
            # extract round number of this directory
            round_number = re.findall(r'\d+', root_base)[0]
            
            # extract all .tif files
            file_list = [f for f in files if f.upper().endswith(tif_suffixes)]
            # append all round files to the dataframe with the correct info
            for file in file_list:
                channel_number = re.findall(r'\d+', file)[0]
                image_path = f"{root}/{file}"
                df = df.append({'Round': round_number, 'Channel': channel_number, 'Image_path': image_path,'Reference': reference_full, 'DAPI' : dapi_full} ,ignore_index=True)
    return df
        


        
    
## Helper function for the entire workflow
def listFileHierarchy(directory):
    hierarchyString = ""
    for root, dirs, files in os.walk(directory):
        level = root.replace(directory, '').count(os.sep)
        indent = ' ' * 4 * (level)
        hierarchyString += '{}{}/\n'.format(indent, os.path.basename(root))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if f.upper().endswith(tif_suffixes):
                hierarchyString+='{}{}\n'.format(subindent, f)
    return hierarchyString

# helper function that adds a backslash to a directory path for consistency
def addBackslash(path):
    if os.path.isdir(path):
        if not path.endswith("/"):
            path += "/"
    return path
#############################
## Test parameters:
## input_dir = /media/tool/starfish_test_data/ExampleInSituSequencing
## Codebook = /media/tool/starfish_test_data/ExampleInSituSequencing/output/codebook.json
## command to run: python main.py /media/tool/starfish_test_data/ExampleInSituSequencing /media/tool/starfish_test_data/ExampleInSituSequencing/output/codebook.json
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

    # parsing the actual arguments
    # rest of the pipeline works with absolute paths behind the scenes for the images to avoid any mistakes.
    input_dir = addBackslash(os.path.abspath(args.input_dir))
    codebook_path = os.path.abspath(args.codebook)
    if not os.path.isdir(input_dir):
        raise ValueError("Inputted directory is not a directory or does not exists")
    if not os.path.isfile(codebook_path):
        raise ValueError("Inputted codebook file does not exist")
    
    
    # parse input images into pandas
    image_df = formatImages(input_dir)
    image_df.to_csv("test.csv")

    # Normalize images
    # registration step 1
    # tiling/paralelizing
    # registrataion step 2
    # spot detection/decoding
    # Visualization

    







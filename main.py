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
import glob
import pandas as pd
import warnings
import re
from icecream import ic

# communISS
from image_processing.normalization.normalization import numpyNormalization
from image_processing.registration.registration_simpleITK import calculateRigidTransform, writeRigidTransformed
from decorators import measureTime

# Variables that are needed in multiples places:
tif_suffixes = ("TIFF","TIF")

## helper functions:

# parseCodebook takes in the filepath and returns a dict that represents the barcodes. 
# (might change this into a pandas later, but for now I'm going to go with )
def parseCodebook(pathToCSV: str):
    """Parses the input codebook csv file into a dict representation of it 

    Parameters
    ----------
    pathToCSV : str
        Path to the input CSV

    Returns
    -------
    Dict
        Dict representation of the given csv file

    Raises
    ------
    Exception
        Raises exception if the columns are not as expected or the input file is not comma delimited.
    """
    codebook_dict = {}
    try:
        with open(pathToCSV, 'r') as file:
            for line in file:
                line_split = line.strip().split(',')
                codebook_dict[line_split[0]] = line_split[1]
    except:
        print("Something went wrong with parsing your codebook. It might not comma delimited?")
    # casual check that the keys don't follow an integer pattern (eg.: 4512), cause that might mean the user switched the two columns.
    if any(key.isdecimal() for key in codebook_dict.keys()):
        raise Exception("Your genes are only combinations of numbers. You might have changed the order of the columns around.")
    return codebook_dict


@measureTime
def formatISSImages(input_dir, silent = False):
    '''This function takes the input_dir that contains the ISS data and returns a pandas Dataframe representing that input dir.
        
        Parameters
        ----------
        input_dir : str
            File path to the images of your ISS project
        silent : boolean
            Boolean to determine if at the end of the function use, it should print out a textual representation of the file hierarchy it found and used in the input_dir.
            False by default, meaning that it will print the hierarchy.
        
        Returns
        -------
        Pandas.DataFrame
            This dataframe represents Tiff images contained in the input dir.
    '''    
    # initialize dataframe
    df = pd.DataFrame(columns=['Round', 'Channel', 'Image_path', 'Reference','DAPI' ])

    # suffix definitions so that recognizing the correct directories is more error robust
    aux_dir_names = ("DO", "AUX_IMAGES", "AUXILLARY_IMAGES")
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
        if "ROUND" in root_base.upper():
            # extract round number of this directory, this is done by finding digits in the dir names
            round_number = re.findall(r'\d+', root_base)[0]
    
            # extract all .tif files
            file_list = [f for f in files if f.upper().endswith(tif_suffixes)]
            # append all round files to the dataframe with the correct info
            for file in file_list:
                channel_number = re.findall(r'\d+', file)[0]
                image_path = f"{root}/{file}"
                df = df.append({'Round': round_number, 'Channel': channel_number, 'Image_path': image_path,'Reference': reference_full, 'DAPI' : dapi_full} ,ignore_index=True)
    if (silent == False):
        print('''Detected tif images are: {}
        If there are files in here that are not supposed to be taken into account for the analysis, we suggest removing them from the input directory
        '''.format(listFileHierarchy(input_dir)))
    if df.empty:
        print("No round image were found, so the naming convention of your round directories is probably not as expected. \n")           
    return df
        


        
    
## Helper function for the entire workflow
def listFileHierarchy(directory: str):
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
def addBackslash(path: str):
    """Adds a backslash to end the given path if not done so already.

    Parameters
    ----------
    path : str
        Given path that needs the backslash added.

    Returns
    -------
    str
        The input path with exactly one backslash in the end.
    """
    if os.path.isdir(path):
        if not path.endswith("/"):
            path += "/"
    return path

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
    image_df = formatISSImages(input_dir=input_dir, silent=True)
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
        
    # create registration dir if it doesn't exist already
    if not os.path.isdir(f"{output_dir}registered/"):
        os.mkdir(f"{output_dir}registered/")
    registered_dir = f"{output_dir}registered/"

    #actually warp the images using the transforms
    for index, row in image_df.iterrows():
        transform_file = f"{transform_dir}transform_r{row['Round']}_c{row['Channel']}.txt"
        registered_file = f"{registered_dir}r{row['Round']}_c{row['Channel']}_registered.tiff"
        writeRigidTransformed(row['Image_path'], transform_file, registered_file)
    

    # tiling/paralelizing
    # registrataion step 2
    # spot detection/decoding
    # Visualization

    







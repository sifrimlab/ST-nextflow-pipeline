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

    MASTER
    |
    |_______Auxillary_images
    |           |____REF_naming_convention
    |           |____DAPI_naming_convention
    |
    |________Round1
        |       |____channel1
        |       |____channel2
        |       |____channel3
        |       |____channel4
        |
        |____Round2
        |       |____channel1
        |       |____channel2
        |       |____channel3
        |       |____channel4
        |
        |____RoundN
        |       |____channel1
        |       |____channel2
        |       |____channel3
        |       |____channel4
        ....
    
    2)  Locate your decoding scheme: you're going to need it. Fill it in in the "codebook" variable, or use it as a parameter when this script is called, depending on how you run this pipeline
        It should be a csv file that is built up as such: (with or without header, that doesn't matter)

        Gene, Code
        BRCA2, 124354


'''
def parseCodebook():
    pass

def formatImages(input_dir):
    '''
        This function takes the input_dir, where it is expected that it contains the ISS data 
    '''

    for root,dir,file in os.walk(input_dir):
        pass
        
    
##Helper function for listing directory structure
def list_files(directory):
    suffixes = ("TIFF","TIF")
    for root, dirs, files in os.walk(directory):
        level = root.replace(directory, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if f.upper().endswith(suffixes):
                print('{}{}'.format(subindent, f))
#Imports
import argparse
import os
import glob
from icecream import ic
#############################
## Test parameters:
## input_dir = /media/tool/starfish_test_data/ExampleInSituSequencing
## Codebook = /media/tool/starfish_test_data/ExampleInSituSequencing/output/codebook.json
## command to run: python main.py /media/tool/starfish_test_data/ExampleInSituSequencing /media/tool/starfish_test_data/ExampleInSituSequencing/output/codebook.json
##############################

if __name__ == '__main__':
    #code the argparser for commandline utility
    parser = argparse.ArgumentParser(prog='communISH', description='Run a rudimentary ISS pipeline')
    #input dir for images
    parser.add_argument('input_dir',help='Path to your input directory')
    #input path for codebook
    parser.add_argument('codebook', help='Path to your codebook')
    #flag to see if the user wants to customize or not
    parser.add_argument('--default',action='store_true', help='Flag to indicate whether to run the default pipeline')
    args = parser.parse_args()

    #parsing the actual arguments
    #rest of the pipeline works with absolute paths behind the scenes for the images to avoid any mistakes.
    input_dir = os.path.abspath(args.input_dir)
    codebook_path = os.path.abspath(args.codebook)
    if not os.path.isdir(input_dir):
        raise ValueError("Inputted directory is not a directory or does not exists")
    if not os.path.isfile(codebook_path):
        raise ValueError("Inputted codebook file does not exist")
    list_files(input_dir)
    # parseImagesIntoDataset
    # Normalize images
    # registration step 1
    # tiling/paralelizing
    # registrataion step 2
    # spot detection/decoding
    # Visualization

    







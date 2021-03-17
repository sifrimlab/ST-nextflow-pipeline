import os
import pandas as pd
import re
import warnings


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


def formatTiledISSImages(input_dir):
    # Create dataframe to be filled in while looping over all files
    df = pd.DataFrame(columns=['Tile', 'Round', 'Channel', 'Image_path', 'Reference','DAPI' ])
    #loop over the entire Tiled dir
    for entry in os.listdir(input_dir):
        # If the current root is a Round dir, we want to extract the files
        if os.path.isdir(os.path.join(input_dir,entry)) and entry.startswith("Round"):
            for file in os.listdir(os.path.join(input_dir,entry)):
                # Extract relevent information for the filenames by first splitting off the .tif extension, then splitting into "_", then taking the last character of each element
                numbers_extracted_from_file_name = [int(element[-1]) if element[-1].isdigit() else element[-1] for element in file.split(".")[0].split("_")]
                round_n, channel_n, tile_n = numbers_extracted_from_file_name
                # The reference and dapi filenames are hardcoded. This shouldn't be a problem because the tiled images are created by the code.
                reference_file = f"Round{round_n}_REF_Tile{tile_n}.tif"
                dapi_file = f"Round{round_n}_DAPI_Tile{tile_n}.tif"
                 # beware that if it's an aux image, channel_n will be a letter, not a digit
                if isinstance(channel_n, int):
                    df = df.append({'Tile': tile_n, 'Round': round_n, 'Channel': channel_n, 'Image_path': os.path.join(input_dir,entry, file), 'Reference': os.path.join(input_dir,entry, reference_file),'DAPI' : os.path.join(input_dir,entry, dapi_file)}, ignore_index=True)
    # Return a sorted df
    return df.sort_values(['Tile', 'Round', 'Channel'])
                
def formatISSImages(input_dir, silent = False, seperate_aux_files_per_round=False):
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
    tif_suffixes = ("TIFF","TIF")

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
        print("Used .tif images are:\n{}\n If there are files in here that are not supposed to be taken into account for the analysis, we suggest removing them from the input directory. \n"
        .format(listUsedFiles(input_dir, df)))
    if df.empty:
        print("No round image were found. The naming convention of your round directories is probably not as expected. \n")           
    return df
    
def listUsedFiles(directory: str, dataframe):
    hierarchyString = ""
    for root, dirs, files in os.walk(directory):
        # calculate level by getting rid of the prefix that every file will have (directory)
        level = root.replace(directory, '').count(os.sep)
        indent = ' ' * 4 * (level)
        base = '{}{}/\n'.format(indent, os.path.basename(root))
        subindent = ' ' * 4 * (level + 1)
        base_added = False
        for f in files:
            if f"{root}/{f}" in dataframe.values:
                if not base_added:
                    hierarchyString+=base
                    base_added = True
                hierarchyString += '{}{}\n'.format(subindent, f)
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

def makeDir(path: str):
    if not os.path.isdir(path):
        os.mkdir(path)


def addDirIntoPath(path, string_to_add, after_which_dir):
    split_path = path.split(after_which_dir)
    # print(split_path)
    split_path.insert(1, after_which_dir + "/" + string_to_add)
    return "".join(split_path)
import numpy as np
import pandas as pd
import re
from skimage import io
from skimage.util import img_as_float
from skimage.measure import label, regionprops, regionprops_table
from skimage.color import label2rgb
import matplotlib.pyplot as plt
from typing import List
from icecream import ic



def createPixelVector(x_coordinate: int,y_coordinate: int, image_list: List[np.array], norm:str ="L2") -> np.array:
    """
    Creates a pixel vector of a pixel by taking that pixel's values across a list of images and normalizing it.

    Parameters
    ----------
        x_coordinate : int
            X coördinate of the pixel
        y_coordinate : int
            Y coördinate of the pixel
        image_list : list[np.array]
            List of images that will be used to track down the pixel's values
        norm : str
            String representing what kind of normalization to perform on the returned array.

    Returns
    -------
        np.array
            np.array representing the intenisty of a given pixel throughout the image list, normalized

    """
    barcode_list = [0 for image in image_list] # start with empty barcode
    for i, actual_image in enumerate(image_list):
        barcode_list[i] = actual_image[y_coordinate, x_coordinate] # first y then x cause array indexing is row, col
    barcode_array = np.array(barcode_list)

    # only normalize if it's not a zero vector, otherwise you get timeout problems
    if norm=="L2" and np.any(barcode_array):
        barcode_array = barcode_array/np.linalg.norm(barcode_array)
    return barcode_array

def createBarcodeVector(barcode: str) -> np.array:
    """
    Creates a normalized numpy representation of a barcode

    Parameters
    ----------
        barcode : str
            String represtentation of a barcode (e.g.: "0010010")

    Returns
    -------
        np.array
            Numpy array representation of that barcode, scaled to unit length.
    """
    # Turn string barcode into array of floats
    array = np.array([float(char) for char in str(barcode)])

    return array/np.linalg.norm(array)


def parseBarcodes(codebook: str, bit_len: int) -> pd.DataFrame:
    """
    Parsed the binary barcodes in a codebook into a dataframe representing the same barcodes.

    Parameters
    ----------
        codebook : str
            Path to codebook.csv
        bit_len : int
            Length of the binary barcodes in the codebook

    Returns
    -------
        pd.DataFrame
            Dataframe representing the codebook with a column of barcodes usable in pixel-based decoding applications.
        

    """
    df = pd.read_csv(codebook)
    df['Barcode'] = [f"{barcode:0{bit_len}}" for barcode in list(df['Barcode'])] #This adds leading 0's back, because converting 001 to df makes it 1 since pandas thinks it's just an int
    df['Index'] = list(range(1,len(df)+1)) # add an index row, to be used to label images later on
    df['Vector'] = [createBarcodeVector(barcode) for barcode in df['Barcode']] # convert string barcodes into int
    return df

def decodePixels(x_dim: int, y_dim: int, codebook: str, bit_len: int, img_path_list: List[str], img_prefix: str, threshold:float = 0.5176) -> pd.DataFrame:
    """
    Decodes a list of images in a pixelwise manner, assigning each pixel to the closest barcode in the codebook.

    Parameters
    ----------
        x_dim : int
            X dimension of input images
        y_dim : int
            Y dimension of input images
        codebook : str
            Path to codebook
        bit_len : int
            Length of the expected bins = number of images in img_path_list
        img_path_list : List[str]
            List of paths to the input images
        img_prefix : str
            Prefix used to sort the input images in ascending order
        threshold : float
            Distance threshold for a pixel vector to be assigned to a barcode vector.

    Returns
    -------
        pd.DataFrame
           Dataframe with every pixel being assigned to the closest barcode in the codebook.

    """
    codebook_df = parseBarcodes(codebook,bit_len)

    # Very important thing here is to sort based on the passed img_prexi, because the iteration needs to be done in order
    r = re.compile(rf"{img_prefix}(\d+)")
    def key_func(m):
        return int(r.search(m).group(1))

    img_path_list.sort(key=key_func)


    # Convert images to float for correct distance comparisan
    image_list =  [img_as_float(io.imread(img)) for img in img_path_list]
    rows_list = [] # rows list is used to store the rows of the df that will be returned
    # Iterate over every pixel
    for x in range(0,x_dim):
        for y in range(0,y_dim):
            # Attribute dics store the key: values of the row's entries
            attribute_dict = {}
            attribute_dict['X'] = x
            attribute_dict['Y'] = y
            pixel_vector = createPixelVector(x,y,image_list)
            minimal_distance = np.inf
            gene_label = ""
            gene_name = ""
            barcode = ""
            for row in codebook_df.itertuples():
                distance = np.linalg.norm(row.Vector - pixel_vector)
                if distance < minimal_distance:
                    minimal_distance = distance
                    gene_label = row.Index
                    gene_name = row.Gene
                    barcode = row.Barcode
            attribute_dict['Barcode'] = barcode
            attribute_dict['Distance'] = minimal_distance
            attribute_dict['Gene'] = gene_name
            # If minimal distance not passing the threshold, it will be labeled as background
            if minimal_distance > threshold:
                gene_label = 0
            attribute_dict['Gene_Label'] = gene_label
            rows_list.append(attribute_dict)
    result_df = pd.DataFrame(rows_list)
    return result_df

# this code assumes that all pixel combinations are present in the decoded_pixels_df
def createSpotsFromDecodedPixels(x_dim: int, y_dim: int, decoded_pixels_df: pd.DataFrame, min_area: int = 4, max_area: int = 10000) -> pd.DataFrame:
    """
    Creates a labeled image using the dataframe created by decodePixels.

    Parameters
    ----------
        x_dim : int
            X dimension of the images used to create the pixel vectors
        y_dim : int
            Y dimension of the images used to create the pixel vectors
        decoded_pixels_df : pd.DataFrame
            Dataframe returned by the decodePixels function
        min_area : int
            Minimum number of neighbouring pixels necessary to form a spot
        max_area : int
            Maximum number of neighbouring pixels necessary to form a spot

    Returns
    -------
        pd.DataFrame
            Dataframe where each row is a detected and decoded spot.
    """
    # Create an empty image to store the gene labels in
    gene_labeled_image = np.zeros((y_dim, x_dim))
    # Create a labeled image using the labels from the dataframe
    for row in decoded_pixels_df.itertuples():
        gene_labeled_image[row.Y, row.X] = row.Gene_Label
    # aggregate the pixels with the same gene label
    region_labeled_image, num_spots = label(gene_labeled_image, background=0, return_num=True)
    # Convert the found "spot" regions into a dataframe
    regions_table = regionprops_table(region_labeled_image, properties=("label", "area", "centroid"))
    regions_df = pd.DataFrame(regions_table)
    # Remove spots that only have an area of min_area and max_area
    regions_df = regions_df[(regions_df['area'] >=min_area) & (regions_df['area'] <= max_area)]
    # Rename some columns to be more meaningful to this usecase.
    regions_df['Y'] = [int(y) for y in list(regions_df['centroid-0'])]
    regions_df['X'] = [int(x) for x in list(regions_df['centroid-1'])]
    regions_df = regions_df.drop(columns=[ "centroid-0", "centroid-1" ])
    regions_df = regions_df.rename(columns={"label":"Spot_label"})


    # combine with the decoded pixels dataframe to add gene name and barcode to the spots
    merged_df = regions_df.merge(decoded_pixels_df, on=["X", "Y"], how="left")
    return merged_df

# threshold based on a 1-bit error in euclidean distance
def decodePixelBased(x_dim, y_dim, codebook, bit_len, img_path_list, img_prefix:str, threshold = 0.5176):
    # First decode each pixel in the image
    decoded_pixels_df = decodePixels(x_dim, y_dim, codebook, bit_len, img_path_list,img_prefix, threshold)
    decoded_pixels_df.to_csv("decoded_pixels_df.csv")

    

    # Then combine neighbouring similarly labeled pixels into spot objects
    decoded_spots_df = createSpotsFromDecodedPixels(x_dim, y_dim, decoded_pixels_df)
    return decoded_spots_df




if __name__=="__main__":
    # x_dim = 2048
    # y_dim = 2048
    # x_dim = 405
    # y_dim = 205

    # tile_nr =  sys.argv[3]
    # tile_nr_int = int(re.findall(r"\d+", tile_nr)[0])
    codebook = "/home/nacho/Documents/communISS/data/merfish/codebook.csv"
    bit_len = 16
    threshold = 0.5176
    image_prefix="merfish_"
    image_path_list = [f"/media/tool/starfish_test_data/MERFISH/processed/cropped/merfish_{i}.tif" for i in range(1, 17)]
    decoded_df = decodePixelBased(405,205, codebook, bit_len, image_path_list,image_prefix,threshold)
    # decoded_df['Tile'] = [tile_nr_int for i in range(0,len(decoded_df))]
    decoded_df.to_csv("decoded.csv", index=False)


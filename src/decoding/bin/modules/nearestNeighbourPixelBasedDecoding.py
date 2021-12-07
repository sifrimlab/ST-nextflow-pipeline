import re
from sklearn.neighbors import NearestNeighbors
from modules.pixelBasedDecoding import parseBarcodes, createBarcodeVector, createPixelVector
from icecream import ic
from skimage import io
from skimage import img_as_float
from skimage.measure import label, regionprops_table
import numpy as np
import pandas as pd

def createCodebookTree(codebook_path: str, bit_len:int, algorithm="ball_tree"):

    def extractVectorsFromCodebook(codebook: str, bit_len: int):
        df = pd.read_csv(codebook)
        ic(type(list(df['Barcode'])[0]), list(df['Barcode'])[0])
        df['Barcode'] = [f"{barcode:0>{bit_len}}" for barcode in list(df['Barcode'])]
        df['Vector'] = [createBarcodeVector(barcode) for barcode in df['Barcode']]
        # array_of_codebook_vectors = np.array(df['Vector'])
        array_of_codebook_vectors = np.vstack([vector for vector in df['Vector']])
        return array_of_codebook_vectors

    array_of_codebook_vectors = extractVectorsFromCodebook(codebook_path, bit_len)
    tree = NearestNeighbors(n_neighbors=1, algorithm='kd_tree').fit(array_of_codebook_vectors)
    return tree, array_of_codebook_vectors


# This takes as input codebook index instead of the codebook, since we want the codebook to only be make once
def findNN(x_dim: int, y_dim: int, codebook_path:str, bit_len: int, img_path_list: str,img_prefix:str,threshold = 0.5176):
    # First create nn tree
    tree, array_of_codebook_vectors = createCodebookTree(codebook_path, bit_len)
    # distances, indices = nn.kneighbors(image_array)
    df = parseBarcodes(codebook_path, bit_len=bit_len)

    # Parse the img_path_list to sort in ascending order, cause they'll be randomized due to nextflow's non-order
    r = re.compile(rf"{img_prefix}(\d+)")
    def key_func(m):
        return int(r.search(m).group(1))
    img_path_list.sort(key=key_func)


    # read all images and convert them to float
    image_list =  [img_as_float(io.imread(img)) for img in img_path_list]
    rows_list = []
    for x in range(0,x_dim):
        for y in range(0,y_dim):
            attribute_dict = {}
            attribute_dict['X'] = x
            attribute_dict['Y'] = y
            pixel_vector = createPixelVector(x,y,image_list)
            minimal_distance_array, index_array = tree.kneighbors(pixel_vector.reshape(1, -1)) # rehsape is necessary because the function expects a 2D array
            minimal_distance, index = minimal_distance_array[0][0], index_array[0][0] # return type of kneighbors is an array, so we gotta unpack the single value
            # We should just have the index of the closest vector now, so we can index the df
            attribute_dict['Barcode'] = df.at[index,'Barcode']# alternative that might be faster: df.iloc[index]['Barcode']
            attribute_dict['Distance'] = minimal_distance
            attribute_dict['Gene'] = df.at[index,'Gene']# alternative that might be faster: df.iloc[index]['Barcode']
            
            # nearest_codebook_vector =np.array(array_of_codebook_vectors[index])
            # Create mask of the vector column, where only 1 will be true
            # mask = df.Vector.apply(lambda x: str(x) == str(nearest_codebook_vector)) # casting to string is necessary to make the comparisan correct
            # match_row = df[mask]
            # for row in match_row.itertuples(): # 'iterate' over rows just so I can get a row object, otherwise indexing the match_row object is even more wonky
                # attribute_dict['Barcode'] =row.Barcode
                # attribute_dict['Distance'] = minimal_distance
                # attribute_dict['Gene'] = row.Gene
            # If minimal distance not passing the threshold, it will be labeled as background
            if minimal_distance > threshold:
                gene_label = 0
            else:
                gene_label = df.at[index,'Index']# some confusion here: 'Index' starts at 1, and is not the same as local variable index
            attribute_dict['Gene_Label'] = gene_label
            rows_list.append(attribute_dict)
    result_df = pd.DataFrame(rows_list)
    return result_df
# this code assumes that all pixel combinations are present in the decoded_pixels_df 
def createSpotsFromDecodedPixels(x_dim, y_dim, decoded_pixels_df, min_area=2, max_area=10000):
    # Create an empty image to store the gene labels in
    gene_labeled_image = np.zeros((y_dim, x_dim))
    for row in decoded_pixels_df.itertuples():
        gene_labeled_image[row.Y, row.X] = row.Gene_Label
    # aggregate the pixels with the same gene label using skimage.measure.label
    region_labeled_image, num_spots = label(gene_labeled_image, background=0, return_num=True)
    # Convert the found "spot" regions into a dataframe
    regions_table = regionprops_table(region_labeled_image, properties=("label", "area", "centroid"))
    regions_df = pd.DataFrame(regions_table)
    # Remove spots that only have an area of min_area and max_area
    regions_df = regions_df[(regions_df['area'] >=min_area) & (regions_df['area'] <= max_area)]
    regions_df['Y'] = [int(y) for y in list(regions_df['centroid-0'])]
    regions_df['X'] = [int(x) for x in list(regions_df['centroid-1'])]
    regions_df = regions_df.drop(columns=[ "centroid-0", "centroid-1" ])
    regions_df = regions_df.rename(columns={"label":"Spot_label"})

    # combine with the decoded pixels dataframe to add gene name and barcode to the spots
    merged_df = regions_df.merge(decoded_pixels_df, on=["X", "Y"], how="left")
    return merged_df

def decodePixelBased(x_dim, y_dim, codebook, bit_len, img_path_list, img_prefix:str, threshold = 0.5176, min_area=2):
    decoded_pixels_df = findNN(x_dim, y_dim, codebook_path=codebook, bit_len=bit_len, img_path_list=img_path_list, img_prefix=img_prefix, threshold=threshold)
    decoded_spots_df = createSpotsFromDecodedPixels(x_dim, y_dim, decoded_pixels_df, min_area = min_area)
    return decoded_spots_df













if __name__ == "__main__":
    codebook_path = "/home/david/Documents/communISS/data/merfish/codebook.csv"
    image_path_list = [f"/media/sda1/starfish_test_data/MERFISH/processed/cropped/merfish_{i}.tif" for i in range(1, 17)]
    bit_len = 16
    threshold = 0.5176
    x_dim, y_dim = (405,205)
    image_prefix="merfish_"
    result_df = decodePixelBased(x_dim, y_dim, codebook=codebook_path, bit_len=bit_len, img_path_list=image_path_list, img_prefix=image_prefix)
    result_df.to_csv("sklearn.csv", index=False)
    # for pixel in image_array:
    #     print(u.get_item_vector((u.get_nns_by_vector(pixel, 1, search_k=-1, include_distances=False))[0])) # This is a way to get the closest vector

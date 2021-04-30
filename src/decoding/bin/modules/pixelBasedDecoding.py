import numpy as np
import pandas as pd
from skimage import io
from skimage.util import img_as_float
from skimage.measure import label, regionprops, regionprops_table
from skimage.color import label2rgb
import matplotlib.pyplot as plt



def createPixelVector(x_coordinate: int,y_coordinate: int, image_list, norm="L2"):
    barcode_list = [0 for image in image_list]
    for i, actual_image in enumerate(image_list):
        barcode_list[i] = actual_image[y_coordinate, x_coordinate]
    barcode_array = np.array(barcode_list)
    if norm=="L2":
        barcode_array = barcode_array/np.linalg.norm(barcode_array)
    return barcode_array

def createBarcodeVector(barcode):
    array = np.array([float(char) for char in str(barcode)]) 
    return array/np.linalg.norm(array) 

def calculateEuclideanDistance(vector1, vector2):
    if len(vector1) != len(vector2):
        print("Vectors not of the same length")
        return 0
    else:
        return np.linalg.norm(vector1 - vector2)

def parseBarcodes(codebook: str, bit_len: int):
    df = pd.read_csv(codebook)
    df['Barcode'] = [f"{barcode:0{bit_len}}" for barcode in list(df['Barcode'])]
    df['Index'] = list(range(1,len(df)+1)) 
    df['Vector'] = [createBarcodeVector(barcode) for barcode in df['Barcode']] 
    return df

def decodePixels(x_dim, y_dim, codebook, bit_len, img_path_list, threshold = 0.5176):
    df = parseBarcodes(codebook,bit_len)
    image_list =  [img_as_float(io.imread(img)) for img in img_path_list]
    rows_list = []
    for x in range(0,x_dim):
        for y in range(0,y_dim):
            attribute_dict = {}
            attribute_dict['X'] = x
            attribute_dict['Y'] = y
            pixel_vector = createPixelVector(x,y,image_list)
            minimal_distance = np.inf
            for row in df.itertuples():
                distance = calculateEuclideanDistance(row.Vector, pixel_vector)
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
            attribute_dict['Label'] = gene_label
            rows_list.append(attribute_dict)
    result_df = pd.DataFrame(rows_list)
    return result_df

# this code assumes that all pixel combinations are present in the decoded_pixels_df 
def labelImage(x_dim, y_dim, decoded_pixels_df, original_image=""):
    gene_labeled_image = np.zeros((y_dim, x_dim))
    for row in decoded_pixels_df.itertuples():
        gene_labeled_image[row.Y, row.X] = row.Label
    region_labeled_image, num_spots = label(gene_labeled_image, background=0, return_num=True)
    regions_table = regionprops_table(region_labeled_image, properties=("label", "area", "centroid"))
    regions_df = pd.DataFrame(regions_table)
    regions_df['Y'] = [int(y) for y in list(regions_df['centroid-0'])]
    regions_df['X'] = [int(x) for x in list(regions_df['centroid-1'])]
    regions_df = regions_df.drop(columns=[ "centroid-0", "centroid-1" ])
    regions_df = regions_df.rename(columns={"label":"Spot_label"})
    print(regions_df.columns)
    print(decoded_pixels_df.columns)
    merged_df = regions_df.merge(decoded_pixels_df, on=["X", "Y"], how="left")

    return merged_df



if __name__=="__main__":
    # 320,86 is a good coordinate to benchmark
    nr_rounds = 8
    nr_channels = 2
    dataDir = "/media/david/Puzzles/starfish_test_data/MERFISH/processed"
    image_path_list = [f"{dataDir}/{i}.tif" for i in range(1,17)]
    image_list = [io.imread(f"{dataDir}/{i}.tif") for i in range(1,17)]
    codebook = "/media/david/Puzzles/starfish_test_data/MERFISH/codebook.csv"
    # parsed_codebook = parseBarcodes(codebook, 16)
    # parsed_codebook.to_csv("parsed_codebook.csv")
    # df = decodePixels(405,205, codebook, 16,image_path_list)
    # df.to_csv("test.csv", index=False)
    df = pd.read_csv("test.csv")
    labelImage(405, 205, df)

    # image testing:
    # pixel_320_86_vector = createPixelVector(320, 86, image_list)
    # print(pixel_320_86_vector)
    # barcode_vector = createBarcodeVector("10101001")


    # distance testing
    # close_vector = createBarcodeVector(10100001)
    # far_vector = createBarcodeVector(11011111)
    # # pixel_vector = createPixelVector(0,0,image_list)
    # close_distance = calculateEuclideanDistance(close_vector, barcode_vector)
    # far_distance = calculateEuclideanDistance(far_vector, barcode_vector)
    # same_distance = calculateEuclideanDistance(barcode_vector, barcode_vector)
    # print(same_distance, close_distance, far_distance)


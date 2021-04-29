import numpy as np
import pandas as pd
from skimage import io



def createPixelVector(x_coordinate: int,y_coordinate: int, image_list):
    barcode_list = [0 for image in image_list]
    for i, actual_image in enumerate(image_list):
        barcode_list[i] = actual_image[y_coordinate, x_coordinate]
    barcode_array = np.array(barcode_list)
    return barcode_array


def createBarcodeVector(barcode):
    return np.array([float(char) for char in str(barcode)])



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

def decodePixels(x_dim, y_dim, codebook, bit_len, img_path_list):
    df = parseBarcodes(codebook,bit_len)
    image_list =  [io.imread(img) for img in img_path_list]
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
            attribute_dict['gene_name'] = gene_name
            attribute_dict['gene_label'] = gene_label
            rows_list.append(attribute_dict)
    result_df = pd.DataFrame(rows_list)
    result_df.to_csv(f"test.csv", index = False)
                    




if __name__=="__main__":
    nr_rounds = 8
    nr_channels = 2
    dataDir = "/media/david/Puzzles/starfish_test_data/MERFISH/processed"
    image_list = [f"{dataDir}/{i}.tif" for i in range(1,17)]
    codebook = "/media/david/Puzzles/starfish_test_data/MERFISH/codebook.csv"

    # parseBarcodes(codebook, 16)
    decodePixels(405,205, codebook, 16,image_list)
    # n_pixels = (io.imread(image_list[0])).size

    # barcode_vector = createBarcodeVector("10101001")
    # close_vector = createBarcodeVector(10100001)
    # far_vector = createBarcodeVector(11011111)
    # pixel_vector = createPixelVector(0,0,image_list)
    # close_distance = calculateDistance(close_vector, barcode_vector)
    # far_distance = calculateDistance(far_vector, barcode_vector)
    # print(close_distance, far_distance)


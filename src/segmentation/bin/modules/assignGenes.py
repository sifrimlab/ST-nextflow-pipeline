from skimage import io
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def assignGenesToCells(labeled_image: str, decoded_genes: str, filter_unrecognized = True):
    image = io.imread(labeled_image) # slicing = [Y,X]
    decoded_df = pd.read_csv(decoded_genes)
    if filter_unrecognized:
        decoded_df = decoded_df[decoded_df['Gene'].isnull()!=True]
    label_column = []
    for row in decoded_df.itertuples():
        label = image[row.Y, row.X]
        label_column.append(label)
    decoded_df['Cell_Label'] = label_column
    return decoded_df


if __name__=='__main__':
    labeled_image = "/media/tool/gabriele_data/1442_OB/maxIP-seperate-channels/results_minsigma1_max_sigma15_stardist_segmentation_no_normalization/segmented/DAPI_padded_tiled_10_labeled.tif"
    # labeled_image = io.imread(labeled_image)
    decoded_genes ="/media/tool/gabriele_data/1442_OB/maxIP-seperate-channels/results_minsigma1_max_sigma15_stardist_segmentation_no_normalization/decoded/decoded_tiled_10.csv" 
    df = pd.read_csv(decoded_genes)
    filtered_df = assignGenesToCells(labeled_image, decoded_genes)
    print(filtered_df)
    # print(np.unique(labeled_image))


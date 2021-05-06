import json
from skimage import io
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def assignGenesToCells(labeled_image: str, decoded_genes: str, cell_properties: str, filter_unrecognized = True):
    image = io.imread(labeled_image) # slicing = [Y,X]
    decoded_df = pd.read_csv(decoded_genes)
    cell_properties_df = pd.read_csv(cell_properties)
    if filter_unrecognized:
        decoded_df = decoded_df[decoded_df['Gene'].isnull()!=True]
    label_column = []
    for row in decoded_df.itertuples():
        label = image[row.Y, row.X]
        if label != 0:
            label = cell_properties_df.loc[cell_properties_df['Image_Label']==label, 'Cell_Label'].iloc[0]
        label_column.append(label)
    decoded_df['Cell_Label'] = label_column
    return decoded_df

def assignGenesToCellsVoronoi(labeled_image: str, decoded_genes: str, cell_properties: str, filter_unrecognized = True):
    image = io.imread(labeled_image) # slicing = [Y,X]
    decoded_df = pd.read_csv(decoded_genes)
    cell_properties_df = pd.read_csv(cell_properties)
    if filter_unrecognized:
        decoded_df = decoded_df[decoded_df['Gene'].isnull()!=True]

    label_column = []

    # Helper function to assign a decoded gene to the closest cell (from cell_properties_df)  to the given excerpt for the decoded_df 
    def assignToNearestCell(decoded_df_row, cell_properties_df):

        # doesn't matter which is x and y, as long as in np.linalg.norm you take the same order
        row_vector = np.array([decoded_df_row.X, decoded_df_row.Y])

        # Initialize closest cell as non existing
        closest_cell_label = 0
        closest_cell_distance = np.inf
        # Iterate over each cell and find the closest one
        for cell in cell_properties_df.itertuples():
            cell_vector = np.array([cell.Center_X, cell.Center_Y])
            distance = np.linalg.norm(row_vector - cell_vector)

            if distance < closest_cell_distance:
                closest_cell_distance = distance
                closest_cell_label = cell.Image_Label
        return closest_cell_label


    # actually assign cells to rows
    for row in decoded_df.itertuples():
        label = image[row.Y, row.X]
        if label == 0:
            label = assignToNearestCell(row, cell_properties_df)
        label = cell_properties_df.loc[cell_properties_df['Image_Label']==label, 'Cell_Label'].iloc[0]
        label_column.append(label)
    decoded_df['Cell_Label'] = label_column
    return decoded_df



if __name__=='__main__':
    # labeled_image = "/media/tool/gabriele_data/1442_OB/maxIP-seperate-channels/results_minsigma1_max_sigma15_stardist_segmentation_no_normalization/segmented/DAPI_padded_tiled_10_labeled.tif"
    # labeled_image = io.imread(labeled_image)
    labeled_image="/media/david/Puzzles/starfish_test_data/MERFISH/seperate_stacks_cropped/results_tiled_whitetophat/segmented/MERFISH_nuclei_padded_tiled_3_labeled.tif" 
    decoded_genes = "/media/david/Puzzles/starfish_test_data/MERFISH/seperate_stacks_cropped/results_tiled_whitetophat/decoded/decoded_tiled_3.csv"
    cell_properties ="/media/david/Puzzles/starfish_test_data/MERFISH/seperate_stacks_cropped/results_tiled_whitetophat/segmented/MERFISH_nuclei_padded_tiled_3_properties.csv" 
    filtered_df = assignGenesToCellsVoronoi(labeled_image, decoded_genes, cell_properties)
    print(filtered_df)
    # print(np.unique(labeled_image))


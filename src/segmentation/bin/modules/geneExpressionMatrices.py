import pandas as pd
from skimage import io
import json
import numpy as np

def createCountMatrix(assigned_genes:str):
    original_df = pd.read_csv(assigned_genes)
    original_df = original_df[original_df.Cell_Label != 0]
    df1 = pd.crosstab(original_df.Gene,original_df.Cell_Label,original_df.Cell_Label,aggfunc='count').fillna(0)
    df2 = original_df.groupby('Gene')['Cell_Label'].value_counts().unstack('Cell_Label', fill_value=0).reset_index()
    return df1

# we're gonna write it like we're assigning globally, not on tiles, so the input is the transformed decoded df, not the one with Tile X and Y coordinates
def createPatchCountMatrix(decoded_df_csv, patch_labeled_image_path, neighbour_dict_path):

    decoded_df = pd.read_csv(decoded_df_csv)
    patch_labeled_image = io.imread(patch_labeled_image_path)
    rows_list = [] # list that will accept each row_dict, and eventually become the gene expression matrix
    with open(neighbour_dict_path, "r") as json_file:
        neighbour_dict = json.load(json_file)
    
    # Actual making of the gene expression matrix

    # We're gonna loop over all patches, they will be stored in the first column 
    # for each patch, go get all pixels from this patch and neighbouring patch, and find out which dots are contained by this immaginary space
    # Yes this is the opposite of a normal count matrix, but this makes this particular code exert a lot more readable, I'll probably just transpose the dataframe at the end
    def getPatchPixels(patch_labeled_image, patch_nr):
        return np.transpose(np.nonzero(patch_labeled_image == patch_nr)) # return ndarray where each row is a coordinate tuple where the patch_nr = true

    # loop over every patch
    for patch in np.unique(patch_labeled_image):
        # create a dict for this patch entry in the expression matrix
        attributes_dict = {}
        attributes_dict["patch"] = f"patch{patch}"
        # calculate its neighbours
        patch_neighbours = neighbour_dict[str(patch)]
        # extract its own coordinates
        coordinate_to_check = getPatchPixels(patch_labeled_image, patch)
        # loop over all neighbours and extract their coordinates to the total coordinates
        for neighbour in patch_neighbours:
            np.vstack((coordinate_to_check, getPatchPixels(patch_labeled_image, neighbour)))
        # Now we have all coordinates, now we check the matches in the decoded df
        for coordinate_row in coordinate_to_check:
            try:
                gene = decoded_df.query('global_X ==@coordinate_row[1] & global_Y ==@coordinate_row[0]')
                attributes_dict[gene] = attributes_dict.get(gene, 0) + 1
            except:
                continue
        rows_list.append(attributes_dict)

    gene_expression_df = pd.DataFrame(rows_list) #rows are patches
    gene_expression_df = gene_expression_df.transpose() # rows are genes
    gene_expression_df.to_csv("patches_gene_expression_matrix.csv")

    return gene_expression_df


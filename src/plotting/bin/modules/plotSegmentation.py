import matplotlib.pyplot as plt
from skimage.util import img_as_ubyte

import numpy as np
import pandas as pd
from skimage import io, color
from skimage.util import img_as_uint, img_as_ubyte, img_as_float64
import matplotlib.pyplot as plt

# tile_image is supposed to be and image with the mask boundaries labeled
def plotAssignedGenes(path_to_assigned_genes: str, path_to_tile_image: str, outfile_prefix):
    assigned_genes = pd.read_csv(path_to_assigned_genes)
    tile_image = io.imread(path_to_tile_image)

    fig, ax = plt.subplots(1,1)
    ax.imshow(tile_image, cmap="gray")
    for row in assigned_genes.itertuples():
        clr = 'green' if str(row.Cell_Label) != '0' else 'red'
        circ = plt.Circle((row.X, row.Y), radius=1, color=clr)
        ax.add_patch(circ)
    plt.axis('off')
    plt.savefig(f"{outfile_prefix}_plotted.svg", format="svg", dpi=1200)

def plotAssignedGenesWRTCell(path_to_assigned_genes: str, path_to_tile_image: str, path_to_cell_propreties, outfile_prefix):
    assigned_genes = pd.read_csv(path_to_assigned_genes)
    tile_image = io.imread(path_to_tile_image)
    properties_df = pd.read_csv(path_to_cell_propreties)
    
    for row in assigned_genes.itertuples():
        clr = properties_df[properties_df["Cell_Label"] ==row.Cell_Label]["Image_Label"].iloc[0]
        if tile_image[row.Y, row.X] == 0:
            tile_image[row.Y, row.X]= clr 

    fig, ax = plt.subplots(1,1)
    ax.imshow(tile_image, cmap="viridis")
    plt.axis('off')
    plt.savefig(f"{outfile_prefix}_plotted.svg", format="svg", dpi=1200)
def plotLabeledImages(path_to_labeled_image: str, overlay_image = ""):
    labeled_image = io.imread(path_to_labeled_image)
    if overlay_image:
        original_image = io.imread(overlay_image)
        original_image = img_as_ubyte(original_image)
    else:
        original_image = None
    colored_image_on_DAPI = color.label2rgb(labeled_image, original_image, bg_label=0)

    return colored_image_on_DAPI


if __name__ == '__main__':

    assigned_genes = "/media/tool/gabriele_data/1442_OB/maxIP-seperate-channels/results_correct_codebook_whiteDisk3_minSigma2_maxSigma20_noNorm_stardistSegmentation_voronoiAssigned/assigned_voronoi/decoded_tiled_29_assigned.csv"
    labeled= "/media/tool/gabriele_data/1442_OB/maxIP-seperate-channels/results_correct_codebook_whiteDisk3_minSigma2_maxSigma20_noNorm_stardistSegmentation_voronoiAssigned/segmented/DAPI_padded_tiled_29_labeled.tif" 
    properties = "/media/tool/gabriele_data/1442_OB/maxIP-seperate-channels/results_correct_codebook_whiteDisk3_minSigma2_maxSigma20_noNorm_stardistSegmentation_voronoiAssigned/segmented/DAPI_padded_tiled_29_properties.csv"
    plotAssignedGenesWRTCell(assigned_genes, labeled, properties, "/media/nacho/Puzzles/results_figures/tile_29_normalAssignment")

import matplotlib.pyplot as plt
from skimage.util import img_as_ubyte
import numpy as np
import pandas as pd
from skimage import io, color
from skimage.util import img_as_uint, img_as_ubyte, img_as_float64
from skimage import draw

# tile_image is supposed to be and image with the mask boundaries labeled
def plotAssignedGenes(path_to_assigned_genes: str, path_to_tile_image: str, outfile_prefix):
    assigned_genes = pd.read_csv(path_to_assigned_genes)
    tile_image = io.imread(path_to_tile_image)

    fig, ax = plt.subplots(1,1)
    ax.imshow(tile_image, cmap="gray")
    for row in assigned_genes.itertuples():
        clr = 'green' if str(row.Cell_Label) != '0' else 'red'
        circ = plt.Circle((row.global_X, row.global_Y), radius=2, color=clr)
        ax.add_patch(circ)
    plt.axis('off')
    plt.savefig(f"{outfile_prefix}_plotted.png", format="png")

def plotAssignedGenesWRTCell(path_to_assigned_genes: str, path_to_tile_image: str, path_to_cell_propreties, original_image_path, outfile_prefix):
    assigned_genes = pd.read_csv(path_to_assigned_genes) # only has Cell_Label
    tile_image = io.imread(path_to_tile_image)
    properties_df = pd.read_csv(path_to_cell_propreties)
    original_image = io.imread(original_image_path)
    original_image = img_as_ubyte(original_image)

    for row in assigned_genes.itertuples():
        # clr = color_dict[properties_df[properties_df["Cell_Label"] ==row.Cell_Label]["Image_Label"].iloc[0]]
        clr = properties_df[properties_df["Cell_Label"] ==row.Cell_Label]["Image_Label"].iloc[0]
        if tile_image[row.Y, row.X] == 0:
            rr, cc = draw.disk((row.Y, row.X), radius=5)
            tile_image[rr, cc]=clr

    overlay = color.label2rgb(tile_image,original_image,bg_label=0)

    _, ax = plt.subplots(1,1)
    ax.imshow(overlay, cmap="viridis")
    plt.axis('off')
    plt.savefig(f"{outfile_prefix}_plotted.png", format="png")

def plotLabeledImages(path_to_labeled_image: str, overlay_image = ""):
    labeled_image = io.imread(path_to_labeled_image)
    if overlay_image:
        original_image = io.imread(overlay_image)
        original_image = img_as_ubyte(original_image)
    else:
        original_image = None
    colored_image_on_DAPI = color.label2rgb(labeled_image, original_image, bg_label=0)

    return colored_image_on_DAPI

import matplotlib.pyplot as plt
from skimage.util import img_as_ubyte

import numpy as np
import pandas as pd
from skimage import io, color
from skimage.util import img_as_uint, img_as_ubyte
import matplotlib.pyplot as plt

# tile_image is supposed to be and image with the mask boundaries labeled
def plotAssignedGenes(path_to_assigned_genes: str, path_to_tile_image: str, outfile_prefix):
    assigned_genes = pd.read_csv(path_to_assigned_genes)
    tile_image = io.imread(path_to_tile_image)

    fig, ax = plt.subplots(1,1)
    ax.imshow(tile_image)
    for row in assigned_genes.itertuples():
        clr = 'green' if str(row.Label) != '0' else 'red'
        circ = plt.Circle((row.X, row.Y), radius=2, color=clr)
        ax.add_patch(circ)
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

    assigned_genes = "/media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/results2/assigned/decoded_tiled_4_assigned.csv"
    labeled= "/media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/results2/segmented/DAPI_padded_tiled_4_labeled.tif" 
    plotAssignedGenes(assigned_genes, labeled)

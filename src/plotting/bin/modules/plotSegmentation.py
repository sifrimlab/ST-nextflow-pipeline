import matplotlib.pyplot as plt
from skimage.util import img_as_ubyte

import numpy as np
import pandas as pd
from skimage import io, color
import matplotlib.pyplot as plt

# tile_image is supposed to be and image with the mask boundaries labeled
def plotAssignedGenes(path_to_assigned_genes: str, path_to_tile_image: str):
    assigned_genes = pd.read_csv(path_to_assigned_genes)
    tile_image = io.imread(path_to_tile_image)

    fig, ax = plt.subplots(1,1)
    ax.imshow(tile_image, cmap="gray")
    for row in assigned_genes.itertuples():
        clr = 'green' if str(row.Gene) != 'nan' else 'red'
        circ = plt.Circle((row.X, row.Y), radius=2, color=clr)
        ax.add_patch(circ)
    return plt
    # fig.savefig('myimage.svg', format='svg', dpi=1200)

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
    original = "/media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/results/tiled_ref/DAPI_padded_tiled_4.tif"
    labeled= "/media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/results/segmented/DAPI_padded_tiled_4_labeled.tif" 
    plotLabeledImages(labeled, original)

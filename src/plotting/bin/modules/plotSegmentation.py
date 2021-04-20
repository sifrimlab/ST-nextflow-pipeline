import matplotlib.pyplot as plt
from icecream import ic
import numpy as np
import pandas as pd
from skimage import io, color


def plotLabeledImages(path_to_labeled_image: str, path_to_dapi_image = "", path_to_reference_image=""):
    labeled_image = io.imread(path_to_labeled_image)
    if path_to_dapi_image:
        original_image = io.imread(path_to_dapi_image)
    else:
        original_image = None
    colored_image_on_DAPI = color.label2rgb(labeled_image, original_image, bg_label=0)

    if path_to_reference_image:
        original_image = io.imread(path_to_reference_image)
        colored_image_on_REF = color.label2rgb(labeled_image, original_image, bg_label=0)
    return colored_image_on_DAPI, colored_image_on_REF if 'colored_image_on_REF' in locals() else None
    
if __name__ == '__main__':
    original = "/media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/results/tiled_ref/DAPI_padded_tiled_4.tif"
    labeled= "/media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/results/segmented/DAPI_padded_tiled_4_labeled.tif" 
    plotLabeledImages(labeled, original)

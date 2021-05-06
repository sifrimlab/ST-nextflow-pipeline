import sys
import re
import os
import pandas as pd
from skimage import io
import numpy as np
from modules.createPseudoCells import createPatchesLabeledImage, createNeighbourDict
from modules.geneExpressionMatrices import createPatchCountMatrix

dapi_image = sys.argv[1]
prefix = os.path.splitext(dapi_image)[0]
transformed_decoded_df =  sys.argv[2]
labeled_patch_image, patches_array = createPatchesLabeledImage(dapi_image, target_row_size=128, target_column_size=128)
createNeighbourDict(patches_array)
neighbour_dict_path = "./patch_neighbours.json"
createPatchCountMatrix(transformed_decoded_df, labeled_patch_image, neighbour_dict_path)

if __name__ == "__main__":
    pass



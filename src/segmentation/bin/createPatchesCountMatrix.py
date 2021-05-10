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
transformed_decoded_df_path =  sys.argv[2]
labeled_patch_image, patches_array = createPatchesLabeledImage(dapi_image, target_row_size=128, target_column_size=128)
createNeighbourDict(patches_array)
neighbour_dict_path = "./patch_neighbours.json"
io.imsave("labeled_image.tif",labeled_patch_image)
labeled_patch_image_path = "labeled_image.tif"

createPatchCountMatrix(transformed_decoded_df_path, labeled_patch_image_path, neighbour_dict_path)


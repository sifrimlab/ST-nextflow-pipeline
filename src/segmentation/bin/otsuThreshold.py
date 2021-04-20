import sys
import re
import os
import pandas as pd
from skimage import io
import numpy as np
from modules.thresholding import otsuThresholding

image_path = sys.argv[1]
prefix = os.path.splitext(image_path)[0]
try:
    # Check if there's a tile number in the image
    tile_nr = re.findall(r"\d+", re.findall(r"tiled_\d+", prefix)[0])[0]
except:
    pass
labeled_image, attributes_df = otsuThresholding(image_path)
# labeled_image is not yet viewable, it's just an int64 image with values 0-#objects, it has no pixel meaning.
# For that you need to call skimage.label2rgb
if 'tile_nr' in locals():
    attributes_df['Tile'] = tile_nr
io.imsave(f"{prefix}_labeled.tif", labeled_image, check_contrast=False)
attributes_df.to_csv(f"{prefix}_properties.csv") 



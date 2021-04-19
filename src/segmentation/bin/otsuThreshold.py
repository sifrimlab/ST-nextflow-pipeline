import sys
import pandas as pd
from skimage import io
import numpy as np
from modules.thresholding import otsuTresholding

image_path = sys.argv[1]
prefix = os.path.splitext(image_path)
labeled_image, attributes_df = otsuTresholding(image_path)
io.imsave(f"{prefix}_labeled.tif", labeled_image)
attriubutes_df.to_csv(f"{prefix}_properties.tif") 



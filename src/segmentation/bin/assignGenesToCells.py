import sys
import re
import os
import pandas as pd
from skimage import io
import numpy as np
from modules.thresholding import assignGenesToCells

decoded_genes = sys.argv[1]
labeled_image_path = sys.argv[2]
prefix = os.path.splitext(decoded_genes)[0]
assigned_df = otsuThresholding(image_path)
assigned_df.to_csv(f"{prefix}_assigned.csv") 



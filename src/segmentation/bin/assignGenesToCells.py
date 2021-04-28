import sys
import re
import os
import pandas as pd
from skimage import io
import numpy as np
from modules.assignGenes import assignGenesToCells

decoded_genes = sys.argv[1]
labeled_image_path = sys.argv[2]
prefix = os.path.splitext(decoded_genes)[0]
assigned_df = assignGenesToCells(labeled_image_path, decoded_genes)
assigned_df.to_csv(f"{prefix}_assigned.csv", index=False) 



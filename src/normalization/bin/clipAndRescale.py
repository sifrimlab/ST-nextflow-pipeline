import sys
import numpy as np
import os
import skimage
from modules.normalization import clipAndNormalize

image_path = sys.argv[1]
percentile = sys.argv[2]
prefix = os.path.splitext(image_path)

clipAndNormalize(image_path, percentile,prefix = prefix )

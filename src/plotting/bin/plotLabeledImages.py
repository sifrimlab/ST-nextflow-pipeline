import matplotlib.pyplot as plt
from modules.plotSegmentation import plotLabeledImages
import numpy as np
import pandas as pd
from skimage import io, color
import sys
import os

labeled_image = sys.argv[1]
prefix = os.path.splitext(labeled_image)[0]

if len(sys.argv) > 2:
    original_image = sys.argv[2]
    overlay_prefix = sys.argv[3]
else:
    original_image = ""
    overlay_prefix=""
colored_image_on_DAPI=plotLabeledImages(labeled_image, overlay_image=original_image)
if overlay_prefix:
    io.imsave(f"{prefix}_overlay_{overlay_prefix}.png", colored_image_on_DAPI)
else:
    io.imsave(f"{prefix}_plotted.png", colored_image_on_DAPI)





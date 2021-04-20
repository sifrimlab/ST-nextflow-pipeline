import matplotlib.pyplot as plt
from modules.plotSegmentation import plotLabeledImages
import numpy as np
import pandas as pd
from skimage import io, color
import sys
import os

labeled_image = sys.argv[1]
prefix = os.path.splitext(labeled_image)[0]
if len(sys.argv)>2:
    dapi_image = sys.argv[2]
else:
    dapi_image = ""
if len(sys.argv)>3:
    ref_image = sys.argv[3]
else:
    ref_image = ""
colored_image_on_DAPI, colored_image_on_REF=plotLabeledImages(labeled_image, dapi_image, ref_image)

for name, image in zip(("DAPI, ref"),(colored_image_on_DAPI, colored_image_on_REF)):
    if image is not None:
        io.imsave(f"{prefix}_overlay_{name}.tif", image)




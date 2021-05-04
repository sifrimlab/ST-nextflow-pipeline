import SimpleITK as sitk
import sys
import os
import re
from modules.calculateTransform import warpImage


##parse arguments
transform = sys.argv[1] 
image = sys.argv[2]

# apply transform:
round_img = sitk.ReadImage(image, sitk.sitkFloat32)
resampled = warpImage(round_img, transform)
prefix = os.path.splitext(image)[0]
sitk.WriteImage(resampled, f"{prefix}_registered.tif")


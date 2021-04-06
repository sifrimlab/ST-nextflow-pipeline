import SimpleITK as sitk
import sys
import os
import re
from icecream import ic
from modules.calculateTransform import calculateTransform, warpImage
# input: 
# REF_padded.tif Round1 Round1_maxIP.tif Round1_c1_padded.tif Round1_c3_padded.tif Round1_c4_padded.tif Round1_c2_padded.tif


##parse arguments
reference = sys.argv[1] 
round_nr = sys.argv[2]
target=sys.argv[3]

img_list = [sys.argv[i] for i in range(4, len(sys.argv))]

# Calculate transform:
fixed = sitk.ReadImage(reference, sitk.sitkFloat32)
moving = sitk.ReadImage(target, sitk.sitkFloat32)
transform = calculateTransform(fixed, moving)

for img in img_list:
    round_img = sitk.ReadImage(img, sitk.sitkFloat32)
    resampled = warpImage(round_img, transform)
    prefix = os.path.splitext(img)[0]
    sitk.WriteImage(resampled, f"{prefix}_registered.tif")

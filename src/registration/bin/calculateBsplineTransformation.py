import SimpleITK as sitk
import sys
import os
import re
from modules.calculateTransform import calculateBsplineTransform

reference = sys.argv[1] 
round_nr = sys.argv[2]
target=sys.argv[3]

# Calculate transform:
fixed = sitk.ReadImage(reference, sitk.sitkFloat32)
moving = sitk.ReadImage(target, sitk.sitkFloat32)
transform = calculateBsplineTransform(fixed, moving)

sitk.WriteTransform(transform, f"{round_nr}_transform.txt")


import sys
import os
from skimage import io
from skimage import img_as_uint

image_path = sys.argv[1]
prefix = os.path.splitext(image_path)[0]
image = io.imread(image_path)

image_16bit = img_as_uint(image)
io.imsave(f"{prefix}_16bit.tif", image_16bit)

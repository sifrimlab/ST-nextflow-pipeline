import os
import sys
import matplotlib.pyplot as plt
from skimage import io
from skimage.utils import img_as_uint
from modules.convolving import gaussianPass

# input parsing

image_path = sys.argv[1]
image = io.imread(image_path)
prefix = os.path.splitext(image_path)[0]
sigma = float(sys.argv[2])
filtered_image = gaussianPass(image_path, sigma)
filtered_image = img_as_uint(filtered_image)
io.imsave(f"{prefix}_filtered.tif", filtered_image)

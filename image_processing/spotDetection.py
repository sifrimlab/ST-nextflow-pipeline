from skimage import io
from skimage.feature import blob_log
import cv2
import os
import sys
import numpy as np
# Beware, not giving min/max sigma's prompts skimage to calculate it, which takes at least twice as long, so for largescale use this is not a good idea
def laplacianOfGaussianBlobDetector(image, min_sigma=None, max_sigma=None):
    if min_sigma is None or max_sigma is None:
        blobs=blob_log(image)
        print("No sigma's received as input for the spot detection. This will increase computation time.")
    else: 
        blobs = blob_log(image, min_sigma, max_sigma)
    return blobs


image = io.imread(sys.argv[1])
prefix = os.path.splitext(sys.argv[1])[0]
min_sigma=sys.argv[2]
max_sigma=sys.argv[3]
np.savetxt(f"{prefix}.csv", laplacianOfGaussianBlobDetector(image, min_sigma, max_sigma), delimiter=',', header="X,Y, Sigma")


import os
import sys
import numpy as np
from skimage import io
from skimage.util import img_as_float, img_as_int
from scipy.signal import convolve2d
import matplotlib.pyplot as plt
from modules.deconvolving import createGaussianKernel, deconvolvePSF

# argparsing 
image_path = sys.argv[1]
prefix = os.path.splitext(image_path)[0]
sigma = float(sys.argv[2])
iterations = int(sys.argv[3])

# kernel size and psf definition adapted from stafish implementation
kernel_size = int(2*np.ceil(2 * sigma)+1)
psf = createGaussianKernel((kernel_size,kernel_size), sigma)

deconvolved = deconvolvePSF(image_path, psf, iterations)
io.imsave(f"{prefix}_deconvolved.tif", deconvolved)


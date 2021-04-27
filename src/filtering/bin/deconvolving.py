import os
import sys
import numpy as np
from skimage import color, data, restoration
from skimage.util import img_as_float
from skimage import io
from scipy.signal import convolve2d
import matplotlib.pyplot as plt

"""
        Starfish:         
        self.sigma = sigma
        self.kernel_size: int = int(2 * np.ceil(2 * sigma) + 1)
        self.psf: np.ndarray = gaussian_kernel(
            shape=(self.kernel_size, self.kernel_size),
            sigma=sigma
"""
def deconvolvePSF(image_path, psf, iterations):
    img = io.imread(image_path)
    # Restore Image using Richardson-Lucy algorithm
    deconvolved_RL = restoration.richardson_lucy(img, psf, iterations)
    return deconvolved_RL

def gaussianKernel(shape, sigma:float):
    m, n = [int((ss - 1.) / 2.) for ss in shape]
    y, x = np.ogrid[-m:m + 1, -n:n + 1]
    kernel = np.exp(-(x * x + y * y) / (2. * sigma * sigma))
    kernel[kernel < np.finfo(kernel.dtype).eps * kernel.max()] = 0
    sumh = kernel.sum()
    if sumh != 0:
        kernel /= sumh
    return kernel

# argparsing 
image_path = sys.argv[1]
prefix = os.path.splitext(image_path)[0]
sigma = float(sys.argv[2])
iterations = int(sys.argv[3])

# kernel size and psf definition adapted from stafish implementation
kernel_size = int(2*np.ceil(2 * sigma)+1)
psf = gaussianKernel((kernel_size,kernel_size), sigma)

deconvolved = deconvolvePSF(image_path, psf, iterations)
io.imsave(f"{prefix}_deconvolved.tif", deconvolved)


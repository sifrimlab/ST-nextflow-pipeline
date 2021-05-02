import numpy as np
from skimage import color, data, restoration
from skimage import io
from skimage.util import img_as_float, img_as_int
import matplotlib.pyplot as plt

"""
        Starfish:         
        self.sigma = sigma
        self.kernel_size: int = int(2 * np.ceil(2 * sigma) + 1)
        self.psf: np.ndarray = gaussian_kernel(
            shape=(self.kernel_size, self.kernel_size),
            sigma=sigma
"""
def calculateKernelSize(sigma):
    return int(2*np.ceil(2 * sigma)+1)

def deconvolvePSF(image_path, psf, iterations):
    img = io.imread(image_path)
    img = img_as_float(img)
    # Restore Image using Richardson-Lucy algorithm
    deconvolved_RL = restoration.richardson_lucy(img, psf, iterations)
    deconvolved_RL = img_as_int(deconvolved_RL)
    return deconvolved_RL

def createGaussianKernel(shape, sigma:float):
    m, n = [int((ss - 1.) / 2.) for ss in shape]
    y, x = np.ogrid[-m:m + 1, -n:n + 1]
    kernel = np.exp(-(x * x + y * y) / (2. * sigma * sigma))
    kernel[kernel < np.finfo(kernel.dtype).eps * kernel.max()] = 0
    sumh = kernel.sum()
    if sumh != 0:
        kernel /= sumh
    return kernel


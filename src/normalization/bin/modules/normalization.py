import numpy as np
import matplotlib.pyplot as plt
from skimage import io
import cv2

def findCutOffPercentile(image_array, percent: int):
    flattened = image_array.flatten()
    flattened = np.sort(flattened)
    cutoff_value = (flattened[int(len(flattened) * percent / 100)])
    return cutoff_value

def cutOffPercentile(image_array, percent: int):
    cutoff_value = findCutOffPercentile(image_array, percent)
    bool_array = np.where(image_array < cutoff_value, 0,image_array)
    float_image = bool_array.astype(float)
    return float_image

def basicNormalize(image_array):
    minimum = np.amin(image_array)
    maximum = np.amax(image_array)
    # Given that minimum will most likely be 0, you're just doing basic dividing by max 
    norm_image = (image_array - minimum) * (1.0 / (maximum - minimum))
    return norm_image

def clipAndNormalize(path_to_image: str, percent_to_clip: int, prefix=""):
    if not 0 <= percent_to_clip <100:
        raise Exception(f"Inputted percentage {percent_to_clip} is not between 0 and 100")
    image = io.imread(path_to_image)
    cut_image = cutOffPercentile(image, percent=percent_to_clip)
    norm_image = basicNormalize(cut_image)
    return norm_image

# not finished yet!
def csbDeepNormalization():
    def normalize(x, pmin=3, pmax=99.8, axis=None, clip=False, eps=1e-20, dtype=np.float32):
        mi = np.percentile(x,pmin,axis=axis,keepdims=True)
        ma = np.percentile(x,pmax,axis=axis,keepdims=True)
        return normalize_mi_ma(x, mi, ma, clip=clip, eps=eps, dtype=dtype)


    def normalize_mi_ma(x, mi, ma, clip=False, eps=1e-20, dtype=np.float32):
        if dtype is not None:
            x   = x.astype(dtype,copy=False)
            mi  = dtype(mi) if np.isscalar(mi) else mi.astype(dtype,copy=False)
            ma  = dtype(ma) if np.isscalar(ma) else ma.astype(dtype,copy=False)
            eps = dtype(eps)

        try:
            import numexpr
            x = numexpr.evaluate("(x - mi) / ( ma - mi + eps )")
        except ImportError:
            x =                   (x - mi) / ( ma - mi + eps )

        if clip:
            x = np.clip(x,0,1)

        return x


    def normalize_minmse(x, target):
        """Affine rescaling of x, such that the mean squared error to target is minimal."""
        cov = np.cov(x.flatten(),target.flatten())
        alpha = cov[0,1] / (cov[0,0]+1e-10)
        beta = target.mean() - alpha*x.mean()
        return alpha*x + beta



import numpy as np
from PIL import Image

def numpyNormalization(image_path):
    image = Image.open(image_path)
    ar = np.asarray(image)
    mn = np.min(ar)
    mx = np.max(ar)
    # given that mn will most likely just be 0, you're effectively dividing by your mx, so basic normalization.
    norm = (ar - mn) * (1.0 / (mx - mn))
    return norm

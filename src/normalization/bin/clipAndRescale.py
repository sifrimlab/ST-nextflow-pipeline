import sys
import numpy as np
import os
from skimage import io
from modules.normalization import clipAndNormalize


if __name__ == "__main__":

    image_path = sys.argv[1]
    percentile = int(sys.argv[2])
    prefix = os.path.splitext(image_path)[0]

    cut_image = clipAndNormalize(image_path, percentile,prefix = prefix )
    cut_image = cut_image.astype("uint16")
    io.imsave(f"{prefix}_normalized.tif", cut_image)
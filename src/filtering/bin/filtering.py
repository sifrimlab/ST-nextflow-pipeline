import os
import cv2
import sys
from skimage.morphology import white_tophat, disk
from skimage import io

def filterWithWhiteTophat(image, radius):
    """Wrapper for skimage's white tophat filter

    Parameters
    ----------
    image : np.ndarray
        Image to be filtered.
    radius: int
        Radius of the morphological disk.
    """
    selem = disk(radius)
    return white_tophat(image,selem)


# Input parsing
img = io.imread(sys.argv[1])
prefix = os.path.splitext(sys.argv[1])[0]
radius = int(sys.argv[2])

# Writing filtered image
cv2.imwrite(f"{prefix}_filtered.tif", filterWithWhiteTophat(img, radius))
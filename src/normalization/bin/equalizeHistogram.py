import os
import sys
from modules.histogramNormalizing import equalizeHist16bit
import cv2

image = sys.argv[1]
prefix = os.path.splitext(image)[0]
equalized_img = equalizeHist16bit(image)
cv2.imwrite(f"{prefix}_equalized.tif", equalized_img)



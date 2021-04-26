import cv2
import numpy as np
image_path = "/media/tool/gabriele_data/1442_OB/maxIP-seperate-channels/DO/DAPI.tif"
image = cv2.imread(image_path, -1)

mean = np.mean(image)
std = np.std(image)
a = (1<<16)*(0.25/std);   # give equalized image a stdDev of 0.25
print(a)
b = (1<<16)*0.5 - a*mean # give equalized image a mean of 0.5
imageEq = a*image+b;


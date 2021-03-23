##opencv solution
import numpy as np
import cv2
import sys



def createComposite(img1, img2):
    A = cv2.cv2.imread(img1, cv2.cv2.IMREAD_ANYDEPTH)
    B = cv2.cv2.imread(img2, cv2.cv2.IMREAD_ANYDEPTH)
    bitDepth = A.dtype
    print(A.dtype, B.dtype)
    zeros = np.zeros(A.shape[:2], dtype=bitDepth)

    ##Don't forget, cv2.cv2 works with a different order sometimes, so it's not RGB it's BGR
    merged = cv2.cv2.merge((zeros,B,A))
    
    return merged

img1 = sys.argv[1]
img2 = sys.argv[2]
cv2.imwrite("composite.tif", createComposite(img1, img2))
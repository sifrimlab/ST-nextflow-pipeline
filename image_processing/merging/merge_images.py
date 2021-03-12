##opencv solution
import numpy as np
import cv2


ref_name = "/home/nacho/Documents/Code/image_processing/image_similarity/imgs/ref_tile48.tif"
target_name = "/home/nacho/Documents/Code/image_processing/image_similarity/imgs/registered_48.tif"

def createComposite(img1, img2):
    A = cv2.cv2.imread(img1, cv2.cv2.IMREAD_ANYDEPTH)
    B = cv2.cv2.imread(img2, cv2.cv2.IMREAD_ANYDEPTH)
    bitDepth = A.dtype
    print(A.dtype, B.dtype)
    zeros = np.zeros(A.shape[:2], dtype=bitDepth)

    ##Don't forget, cv2.cv2 works with a different order sometimes, so it's not RGB it's BGR
    merged = cv2.cv2.merge((zeros,B,A))
    
    return merged

import cv2
import numpy as np
import matplotlib.pyplot as plt

def equalizeHist16bit(image_path):
    img_tif=cv2.imread("scan.tif",cv2.IMREAD_ANYDEPTH)
    img = np.asarray(img_tif)
    flat = img.flatten()
    hist = get_histogram(flat,65536)
    #plt.plot(hist)

    cs = cumsum(hist)
    # re-normalize cumsum values to be between 0-255

    # numerator & denomenator
    nj = (cs - cs.min()) * 65535
    N = cs.max() - cs.min()

    # re-normalize the cdf
    cs = nj / N
    cs = cs.astype('uint16')
    img_new = cs[flat]
    #plt.hist(img_new, bins=65536)
    #plt.show(block=True)
    img_new = np.reshape(img_new, img.shape)
    cv2.imwrite("contrast.tif",img_new)

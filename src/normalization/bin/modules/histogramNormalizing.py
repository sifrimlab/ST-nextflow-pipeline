import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from skimage.exposure import match_histograms
from skimage.util import img_as_uint
# create our cumulative sum function
def cumsum(a):
    a = iter(a)
    b = [next(a)]
    for i in a:
        b.append(b[-1] + i)
    return np.array(b)

# create our own histogram function
def get_histogram(image, bins):
    # array with size of bins, set to zeros
    histogram = np.zeros(bins)
    # loop through pixels and sum up counts of pixels
    for pixel in image:
        histogram[pixel] += 1
    # return our final result
    return histogram

def equalizeHist8bit(image_path: str):
    img = cv2.imread(image_path, 0)
    equalized_img = cv2.equalizeHist(img)
    plt.imshow(equalized_img, cmap="gray")
    plt.show()

def equalizeHist16bit(image_path):
    img_tif = cv2.imread(image_path, cv2.IMREAD_ANYDEPTH)
    img = np.asarray(img_tif)
    flat = img.flatten()
    hist = get_histogram(flat, 65536)

    cumulative_sum = cumsum(hist)
    # re-normalize cumsum values to be between 0-255

    # numerator & denomenator
    nj = (cumulative_sum - cumulative_sum.min()) * 65535
    N = cumulative_sum.max() - cumulative_sum.min()

    # re-normalize the cdf
    cumulative_sum = nj / N
    cumulative_sum = cumulative_sum.astype('uint16')
    img_new = cumulative_sum[flat]
    img_new = np.reshape(img_new, img.shape)
    return img_new

def matchHistograms(image_ref_path, image_target_path):
    reference = io.imread(image_ref_path)
    print(reference.dtype, reference.shape)
    target = io.imread(image_target_path)
    print(target.dtype, target.shape)

    matched = match_histograms(target, reference)
    print(matched.dtype, matched.shape)
    plt.imshow(matched, cmap='gray')
    plt.show()
    

    # return matched


if __name__ == '__main__':
    reference = "/media/nacho/Puzzles/gabriele_data/hippo_3/Round1/Round1_c2_maxIP.tif"
    target = "/media/nacho/Puzzles/gabriele_data/hippo_3/Round1/Round1_c1_maxIP.tif"
    matchHistograms(reference, target)
    # io.imsave("/media/nacho/Puzzles/gabriele_data/hippo_3/Round1/Round1_c1_maxIP_matched.tif", matched)

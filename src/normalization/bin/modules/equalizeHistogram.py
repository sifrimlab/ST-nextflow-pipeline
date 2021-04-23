import cv2
import numpy as np
import matplotlib.pyplot as plt
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


if __name__ == '__main__':
    # normal_image = "/media/david/Puzzles/gabriele_data/1442_OB/DO/REF.tif"
    normal_image = "/media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/Round1/Round1_c5.TIF"
    equalizeHist8bit(normal_image)


import cv2
import numpy as np
import matplotlib.pyplot as plt
from icecream import ic
from skimage import io
from skimage.exposure import match_histograms
from skimage.util import img_as_uint
from PIL import Image
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
    ic(reference.dtype, reference.shape, type(reference))
    target = io.imread(image_target_path)
    ic(target.dtype, target.shape, type(target))

    matched = match_histograms(target, reference)
    ic(matched.dtype, matched.shape, type(matched))
    data = Image.fromarray(matched)
    # saving the final output 
    # as a PNG file
    data.save('/media/nacho/Puzzles/gabriele_data/hippo_3/Round1/Round1_c1_maxIP_matched.tif')
    # plt.imshow(matched, cmap='gray')
    # plt.show()
    # io.imsave("hippo_3_r1c3_tile28.png", reference)
    # io.imsave("hippo_3_r1c1_tile28.png", target)
    # io.imsave("hippo_3_r1c1_matched_tile28.png", matched)
    

    # return matched

## Everything below here is from https://towardsdatascience.com/histogram-matching-ee3a67b4cbc1
## To be adapted into a custom 32-bit histogram matching
def generate_histogram(img, do_print):
"""
@params: img: can be a grayscale or color image. We calculate the Normalized histogram of this image.
@params: do_print: if or not print the result histogram
@return: will return both histogram and the grayscale image 
"""
if len(img.shape) == 3: # img is colorful, so we convert it to grayscale
    gr_img = np.mean(img, axis=-1)
else:
    gr_img = img
'''now we calc grayscale histogram'''
gr_hist = np.zeros([256])

for x_pixel in range(gr_img.shape[0]):
    for y_pixel in range(gr_img.shape[1]):
        pixel_value = int(gr_img[x_pixel, y_pixel])
        gr_hist[pixel_value] += 1
        
'''normalizing the Histogram'''
gr_hist /= (gr_img.shape[0] * gr_img.shape[1])
if do_print:
    print_histogram(gr_hist, name="n_h_img", title="Normalized Histogram")
return gr_hist, gr_img

def print_histogram(_histrogram, name, title):
plt.figure()
plt.title(title)
plt.plot(_histrogram, color='#ef476f')
plt.bar(np.arange(len(_histrogram)), _histrogram, color='#b7b7a4')
plt.ylabel('Number of Pixels')
plt.xlabel('Pixel Value')
plt.savefig("hist_" + name)

def find_value_target(val, target_arr):
    key = np.where(target_arr == val)[0]

    if len(key) == 0:
        key = find_value_target(val+1, target_arr)
        if len(key) == 0:
            key = find_value_target(val-1, target_arr)
    vvv = key[0]
    return vvv


def match_histogram(inp_img, hist_input, e_hist_input, e_hist_target, _print=True):
    '''map from e_inp_hist to 'target_hist '''
    en_img = np.zeros_like(inp_img)
    tran_hist = np.zeros_like(e_hist_input)
    for i in range(len(e_hist_input)):
        tran_hist[i] = find_value_target(val=e_hist_input[i], target_arr=e_hist_target)
    print_histogram(tran_hist, name="trans_hist_", title="Transferred Histogram")
    '''enhance image as well:'''
    for x_pixel in range(inp_img.shape[0]):
        for y_pixel in range(inp_img.shape[1]):
            pixel_val = int(inp_img[x_pixel, y_pixel])
            en_img[x_pixel, y_pixel] = tran_hist[pixel_val]
    '''creating new histogram'''
    hist_img, _ = generate_histogram(en_img, print=False, index=3)
    print_img(img=en_img, histo_new=hist_img, histo_old=hist_input, index=str(3), L=L)



if __name__ == '__main__':
    reference = "/media/nacho/Puzzles/gabriele_data/hippo_3/Round1/Round1_c2_maxIP.tif"
    target = "/media/nacho/Puzzles/gabriele_data/hippo_3/Round1/Round1_c1_maxIP.tif"
    matchHistograms(reference, target)
    # io.imsave("/media/nacho/Puzzles/gabriele_data/hippo_3/Round1/Round1_c1_maxIP_matched.tif", matched)

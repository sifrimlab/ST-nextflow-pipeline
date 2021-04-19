from skimage import io
import math
from skimage.feature import blob_log
import os
import matplotlib.pyplot as plt
from skimage.morphology import white_tophat, disk
import numpy as np

img_path = "/media/tool/gabriele_data/1442_OB/maxIP-seperate-channels/results/tiled_ref/REF_padded_tiled_29.tif"
image = io.imread(img_path)
empty_image = np.zeros(image.shape)
# empty_raw_image = np.zeros(image.shape)


def whiteFilter(image, radius):
    selem = disk(radius)
    image = white_tophat(image,selem)
    return image

def detectSpots(image, min_sigma=1, max_sigma=10):
    image = image.astype('uint8')
    blobs = blob_log(image, min_sigma=int(min_sigma), max_sigma=int(max_sigma))
    return blobs.astype(int)

filtered_image = whiteFilter(image, 15)

# raw_blobs = detectSpots(image, 1,10)
# sigmas = raw_blobs[:,2]
smallest_blobs = detectSpots(filtered_image, 1,10)
smal_blobs = detectSpots(filtered_image, 1,20)
bigger_blobs = detectSpots(filtered_image, 2,10)
biggest_blobs = detectSpots(filtered_image, 2,20)
# sigmas = blobs[:,2]
# print(np.amax(sigmas))
# average = np.mean(sigmas)
# stdev = np.std(sigmas)
# interval = (math.floor(average-stdev), math.ceil(average+stdev))
# is_between_list = [interval[0] <= sigma <= interval[1] for sigma in sigmas]


fig, axs = plt.subplots(2,2)
axs[0,0].imshow(image, cmap='gray')
axs[0,0].set_title("1,10")
for x in smallest_blobs:
        circ = plt.Circle((x[1], x[0]), radius=1)
        axs[0,0].add_patch(circ)

axs[0,1].imshow(filtered_image, cmap='gray')
axs[0,1].set_title("1,20")
for x in smal_blobs:
        circ = plt.Circle((x[1], x[0]), radius=1)
        axs[0,1].add_patch(circ)

axs[1,0].imshow(filtered_image, cmap='gray')
axs[1,0].set_title("2,10")
for x in bigger_blobs:
        circ = plt.Circle((x[1], x[0]), radius=1)
        axs[1,0].add_patch(circ)

axs[1,1].imshow(filtered_image, cmap='gray')
axs[1,1].set_title("2,20")
for x in biggest_blobs:
        circ = plt.Circle((x[1], x[0]), radius=1)
        axs[1,1].add_patch(circ)
plt.show()

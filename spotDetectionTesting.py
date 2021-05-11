from skimage import io
from skimage import color
from skimage.measure import label
import math
from skimage.feature import blob_log
import os
import matplotlib.pyplot as plt
from skimage.morphology import white_tophat, disk, extrema
import numpy as np

img_path = "/media/tool/gabriele_data/161230_161220_3_1/maxIP-seperate-channels/results/tiled_DO/REF_padded_tiled_29.tif"
image = io.imread(img_path)
# plt.imshow(image)
# plt.show()
empty_image = np.zeros(image.shape)
# empty_raw_image = np.zeros(image.shape)


def whiteFilter(image, radius):
    selem = disk(radius)
    image = white_tophat(image,selem)
    return image

def detectSpots(image, min_sigma, max_sigma):
    image = image.astype('uint8')
    blobs = blob_log(image, min_sigma=int(min_sigma), max_sigma=int(max_sigma))
    return blobs.astype(int)

def localMaximaDetectSpots(image):
    local_maxima = extrema.local_maxima(image)
    label_maxima = label(local_maxima)
    overlay = color.label2rgb(label_maxima, image, alpha=0.7, bg_label=0,
                              bg_color=None, colors=[(1, 0, 0)])
    # plt.imshow(overlay)
    # plt.show()

def hMaximaDetectSpots(image):
    h = 100
    h_maxima = extrema.h_maxima(image, h)
    print(h_maxima)
    label_h_maxima = label(h_maxima)
    overlay_h = color.label2rgb(label_h_maxima, image, alpha=0.7, bg_label=0,
                                bg_color=None, colors=[(1, 0, 0)])

    # fig,axs = plt.subplots(1,2)
    plt.imshow(overlay_h)
    plt.show()


# Filter image
filtered_image = whiteFilter(image, 3)
io.imsave("test.tif", filtered_image)
# plt.imshow(filtered_image)
# plt.show()

# Actual spotdetection

# # local maxima
# hMaximaDetectSpots(filtered_image)

# raw_blobs = detectSpots(image, 1,10)
# smallest_blobs = detectSpots(filtered_image, 1,10)
# smal_blobs = detectSpots(filtered_image, 1,20)
# bigger_blobs = detectSpots(filtered_image, 2,10)
biggest_blobs = detectSpots(filtered_image, 3,5)
print(len(biggest_blobs))

#side-by-side visualization
# fig, axs = plt.subplots(1,2)

# axs[0].imshow(filtered_image, cmap='gray')
# axs[1].imshow(filtered_image, cmap='gray')
# for x in biggest_blobs:
#         circ = plt.Circle((x[1], x[0]), radius=x[2])
#         axs[1].add_patch(circ)
# plt.show()

# one vizualisation
fig, axs = plt.subplots(1,1)
axs.imshow(filtered_image, cmap='gray')
for x in biggest_blobs:
    circ = plt.Circle((x[1], x[0]), radius=x[2])
    axs.add_patch(circ)
plt.show()



# All visualization

# fig, axs = plt.subplots(2,2)
# axs[0,0].imshow(filtered_image, cmap='gray')
# axs[0,0].set_title("1,10")
# for x in smallest_blobs:
#     circ = plt.Circle((x[1], x[0]), radius=2)
#     axs[0,0].add_patch(circ)

# axs[0,1].imshow(filtered_image, cmap='gray')
# axs[0,1].set_title("1,20")
# for x in smal_blobs:
#         circ = plt.Circle((x[1], x[0]), radius=2)
#         axs[0,1].add_patch(circ)

# axs[1,0].imshow(filtered_image, cmap='gray')
# axs[1,0].set_title("2,10")
# for x in bigger_blobs:
#         circ = plt.Circle((x[1], x[0]), radius=2)
#         axs[1,0].add_patch(circ)

# axs[1,1].imshow(filtered_image, cmap='gray')
# axs[1,1].set_title("2,20")
# for x in biggest_blobs:
#         circ = plt.Circle((x[1], x[0]), radius=2)
#         axs[1,1].add_patch(circ)
# plt.show()

import os
import sys
from skimage import io
from skimage.measure import label
from skimage import draw
import math
from skimage.feature import blob_log
import matplotlib.pyplot as plt
from skimage.morphology import white_tophat, disk, extrema
import numpy as np

image_path = sys.argv[1]
image = io.imread(image_path)
tophat_filter_radius=  sys.argv[2]
min_sigma =  sys.argv[3]
max_sigma =   sys.argv[4]

if len(sys.argv) > 4:
    num_sigma = sys.argv[5]
else:
    num_sigma = 10

if len(sys.argv) > 5:
    threshold = sys.argv[6]
else:
    threshold = 0.2 

if len(sys.argv) > 6:
    overlap = sys.argv[7]
else:
    overlap = 0.5 

# empty_image = np.zeros(image.shape)


def whiteFilter(image, radius):
    selem = disk(radius)
    image = white_tophat(image,selem)
    return image


def detectSpotsLoG(image, min_sigma=1, max_sigma=10, num_sigma=10, threshold=0.2, overlap=0.5):
    image = image.astype('uint8')
    blobs = blob_log(image, min_sigma, max_sigma, num_sigma, threshold, overlap)
    return blobs

filtered_image = whiteFilter(image, tophat_filter_radius)


blobs = blob_log(image, min_sigma=min_sigma, max_sigma= max_sigma, num_sigma=num_sigma, threshold=threshold, overlap=overlap)
initial_number = len(blobs)


# QC based on sigma's
average_sigma = np.mean(blobs[:,2])
stdev_sigma = np.std(blobs[:,2])
upper_bound =math.ceil(average_sigma +(2*stdev_sigma))
lower_bound =math.floor(average_sigma -(2*stdev_sigma))
mask = np.where(np.logical_or(blobs[:,2] > upper_bound, blobs[:,2] < lower_bound),  False, True)
blobs = blobs[mask]
after_filtering = len(blobs)


print(f"Number of blobs found: {len(blobs)}, {initial_number - after_filtering} blobs were left out due to sigma filtering")

# side-by-side visualization
 fig, axs = plt.subplots(1,2)

 axs[0].imshow(filtered_image, cmap='gray')
 axs[1].imshow(filtered_image, cmap='gray')
 for x in blobs:
         circ = plt.Circle((x[1], x[0]), radius=x[2], color="w")
         axs[1].add_patch(circ)
 plt.show()

# one vizualisation
fig, axs = plt.subplots(1,1)
axs.imshow(filtered_image, cmap='gray')
for x in bigger_blobs:
    try:
        circ = draw.disk((x[0],x[1] ), radius=x[2]) 
        filtered_image[circ]=255
    except:
        pass

    # circ = plt.Circle((x[1], x[0]), radius=x[2], color='w')
    # axs.add_patch(circ)
# plt.axis('off')
# plt.show()



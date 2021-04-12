import numpy as np
import matplotlib.pyplot as plt
from skimage import io
image = "/home/david/Documents/image_registration/reference.tif"

def findCutOffPercentile(image_array, percent: int):
    flattened = image_array.flatten()
    flattened = np.sort(flattened)
    cutoff_value = (flattened[int(len(flattened) * percent / 100)])
    return cutoff_value
image = io.imread(image)
cutoff_value = findCutOffPercentile(image, 80)
test = np.where(image < cutoff_value)
print(test[1]  ) # those are the indices

 #test_array = np.clip()

 #plt.imshow(image)
 #plt.show()

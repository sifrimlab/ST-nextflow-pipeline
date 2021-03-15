from image_processing.image_similarity.image_similarities import getHistogram
import matplotlib.pyplot as plt
from skimage import io
img_list = ["/media/tool/starfish_test_data/MERFISH/seperate_stacks/16-bit/MERFISH_primary-00{:0=2d}.tif".format(i) for i in range(1,17)]

# io.imsave("test.tiff", createComposite(img_list[0], img_list[1]))

##normalization testspace

f, axarr = plt.subplots(4, 4)
index = 0
for i in range(0,4):
    for j in range(0,4):
        hist = getHistogram(img_list[index])
        axarr[i,j].plot(hist)
        axarr[i,j].set_title(f'Axis [{i},{j}]: index {index}')
        index +=1
plt.show()

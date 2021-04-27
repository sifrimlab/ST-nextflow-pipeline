from skimage.filters import gaussian
import matplotlib.pyplot as plt
from skimage import io


image_path = "/media/david/Puzzles/starfish_test_data/MERFISH/seperate_stacks/Round_1_c1_MERFISH.tif"
image = io.imread(image_path)

filtered_image = gaussian(image, sigma=3)

fig,axs = plt.subplots(1,2)
axs[0].imshow(image)
axs[1].imshow(filtered_image)
plt.show()


import numpy as np
from skimage import io
import os
# def maxIP(img1, img2):
#     if not isinstance(img1, np.ndarray):
#         img1 = io.imread("/media/david/Puzzles/starfish_test_data/MERFISH/seperate_stacks/MERFISH_primary-0001.tif")
#     if not isinstance(img1, np.ndarray):
#         img2 = io.imread("/media/david/Puzzles/starfish_test_data/MERFISH/seperate_stacks/MERFISH_primary-0005.tif")
#     maxIP= np.maximum(img1, img2)
#     return maxIP


# img_list= ["/media/david/Puzzles/starfish_test_data/MERFISH/seperate_stacks/MERFISH_primary-0001.tif","/media/david/Puzzles/starfish_test_data/MERFISH/seperate_stacks/MERFISH_primary-0005.tif", "/media/david/Puzzles/starfish_test_data/MERFISH/seperate_stacks/MERFISH_primary-0007.tif"]
def maxIPstack(img_list):
    parsed_list = img_list
    parsed_list = [img if isinstance(img, np.ndarray) else io.imread(img) for img in img_list]
    # now all elements in parsed_list are ndarrays
    maxIP = np.maximum.reduce(parsed_list)
    return maxIP


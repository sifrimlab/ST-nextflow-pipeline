from image_processing.similarity.image_similarities import getHistogram
from image_processing.normalization.normalization import numpyNormalization
import matplotlib.pyplot as plt
from skimage import io
img_list = ["/media/tool/starfish_test_data/MERFISH/seperate_stacks/16-bit/MERFISH_primary-00{:0=2d}.tif".format(i) for i in range(1,17)]

## normalization testspace
# start with creating an intensity histogram for all
# f, axarr = plt.subplots(4, 4)
# index = 0
# for i in range(0,4):
#     for j in range(0,4):
#         hist = getHistogram(img_list[index])
#         axarr[i,j].plot(hist)
#         axarr[i,j].set_title(f'Axis [{i},{j}]: index {index}')
#         index +=1
# plt.show()

# now we normalize with numpy
# img_list_normalized = []
# for i, img in enumerate(img_list):
#     # img_list_normalized.append(numpyNormalization0to1(img))
#     io.imsave("/media/tool/starfish_test_data/MERFISH/seperate_stacks/16-bit/normalized/0to1/MERFISH_primary-00{:0=2d}.tif".format(i+1), numpyNormalization0to1(img))


# img_list_normalized = ["/media/tool/starfish_test_data/MERFISH/seperate_stacks/16-bit/normalized/MERFISH_primary-00{:0=2d}.tif".format(i) for i in range(1,17)]
# f, axarr = plt.subplots(4, 4)
# index = 0
# for i in range(0,4):
#     for j in range(0,4):
#         hist = getHistogram(img_list_normalized[index])
#         axarr[i,j].plot(hist)
#         axarr[i,j].set_title(f'Axis [{i},{j}]: index {index}')
#         index +=1
# plt.show()



## Tiling testing:
# from skimage import io
# import cv2
# import math
# from decorators import measureTime

# @measureTime
# def skimageTest():
#     img = io.imread("/media/tool/starfish_test_data/ExampleInSituSequencing/Round1/c4.TIF", 1) # 512x512

#     # Don't forget, cv2 works with shape = (y, x)
#     img_shape = img.shape

#     tile_size = (665, 490)
#     offset = (665, 490)

#     for i in range(int(math.ceil(img_shape[0]/(offset[1] * 1.0)))):
#         for j in range(int(math.ceil(img_shape[1]/(offset[0] * 1.0)))):
#             cropped_img = img[offset[1]*i:min(offset[1]*i+tile_size[1], img_shape[0]), offset[0]*j:min(offset[0]*j+tile_size[0], img_shape[1])]
#             # Debugging the tiles
#             io.imsave("debug_" + str(i) + "_" + str(j) + ".png", cropped_img)

# @measureTime
# def cv2Test():
#     img = cv2.imread("/media/tool/starfish_test_data/ExampleInSituSequencing/Round1/c4.TIF", 1) # 512x512

#     # Don't forget, cv2 works with shape = (y, x)
#     img_shape = img.shape

#     tile_size = (665, 490)
#     offset = (665, 490)

#     for i in range(int(math.ceil(img_shape[0]/(offset[1] * 1.0)))):
#         for j in range(int(math.ceil(img_shape[1]/(offset[0] * 1.0)))):
#             cropped_img = img[offset[1]*i:min(offset[1]*i+tile_size[1], img_shape[0]), offset[0]*j:min(offset[0]*j+tile_size[0], img_shape[1])]
#             # Debugging the tiles
#             cv2.imwrite("debug_" + str(i) + "_" + str(j) + ".png", cropped_img)
# skimageTest()
# cv2Test()
# conclusion: cv2 is significantly faster

## testing for optimal divison

# @measureTime
# def findOptimalDivisor(number, target_quotient):
#     divisors = [i for i in range(1,number) if number % i==0]
#     quotients = [number/divisor for divisor in divisors]
#     min_loss = min(quotients, key=lambda x:abs(x-target_quotient))
#     best_divisor = number/min_loss
#     return best_divisor
# findOptimalDivisor(3066, 1000)

##Testing for white tophat
# from skimage import io
# from skimage.morphology import white_tophat


# img = io.imread("/media/tool/starfish_test_data/ExampleInSituSequencing/Round1/c4.TIF")
# filtered = white_tophat(img)

# fig = plt.figure()
# plt.gray()
# ax = fig.add_subplot(1, 2, 1)
# imgplot = plt.imshow(img)
# ax.set_title('Original')
# ax = fig.add_subplot(1, 2, 2)
# imgplot = plt.imshow(filtered)
# ax.set_title('filtered')
# plt.show()

## playing with os.path.join
# import os
# base_dir = "/media/tool/starfish_test_data/ExampleInSituSequencing"
# new_dir = "formatted"
# print(os.path.join(base_dir, new_dir)+"/")

## playing with iterating over pandas
# import pandas as pd
# df = pd.read_csv("tiled_images.csv")
# for row in df.itertuples():
#     print(row.DAPI)

##Test with adapting pandas dataframe
# import pandas as pd
# df = pd.read_csv("./tiled_images.csv")
# def addDirIntoPath(path, string_to_add, after_which_dir):
#     split_path = path.split(after_which_dir)
#     # print(split_path)
#     split_path.insert(1, after_which_dir + "/" + string_to_add)
#     return "".join(split_path)
# df['Image_path'] = df['Image_path'].apply(addDirIntoPath, args=("filtered","tiled"))
# df.to_csv("adapted.csv")

## testing blobdetectors
from skimage.feature import blob_log
import cv2

img_name = "/media/david/Puzzles/starfish_test_data/communISS_output/tiled/filtered/Round1/Round1_Channel5_Tile4.tif"
img = cv2.imread(img_name,-1)
array = blob_log(img,0.5,3)
print(array[:,0:2])


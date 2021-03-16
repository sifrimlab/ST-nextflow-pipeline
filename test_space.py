from image_processing.image_similarity.image_similarities import getHistogram
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




## Testing with elements in dataframe
import pandas as pd
df = pd.read_csv("images.csv")
if "/media/tool/starfish_test_data/ExampleInSituSequencing/DO/REF.TIF" in df.values:
    print("yup")
import numpy as np
import math
from skimage import io
from skimage.util import img_as_int
import matplotlib.pyplot as plt

def createPatchesLabeledImage(dapi_tile_path):
    target_row_size = 128
    target_column_size = 128

    #extract original dims
    image = io.imread(dapi_tile_path)
    row_size,column_size = image.shape
    empty_image = np.zeros(image.shape)

    # Create patches grid
    patches_grid_size_column = int(math.floor(column_size / target_row_size * 1.0))
    patches_grid_size_row = int(math.floor(row_size / target_row_size * 1.0))
    patches_number = (patches_grid_size_column * patches_grid_size_row) 
    patches_vector = np.array(list(range(1,patches_number+1)))
    patches_array = np.reshape(patches_vector, (patches_grid_size_row, patches_grid_size_column))

    # For each patch
    for row in range(0,1): # patches_grid_size_row
        for column in range(1,2): # patches_grid_size_column
            patch_label = int(patches_array[row,column])
            # Inside each patch, for each pixel inside the patch
            for pixel_row in range(0, target_row_size):
                for pixel_column in range(0,target_column_size):
                    row_coordinate = pixel_row + (row * target_row_size)
                    column_coordinate = pixel_column + (column* target_column_size)
                    empty_image[row_coordinate, column_coordinate]=patch_label
    print(np.unique(empty_image))

    # for i in range(int(math.ceil(row_size / target_y_size * 1.0))):
    #     for j in range(int(math.ceil(column_size / target_x_size * 1.0))):
    plt.imshow(empty_image)
    plt.show()

if __name__ == "__main__":
    dapi_tile_path = "/media/tool/gabriele_data/1442_OB/maxIP-seperate-channels/results_correct_codebook_whiteDisk3_minSigma2_maxSigma20_noNorm_stardistSegmentation/tiled_DO/DAPI_padded_tiled_13.tif"
    createPatchesLabeledImage(dapi_tile_path)




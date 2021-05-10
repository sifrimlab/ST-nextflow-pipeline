import json
import numpy as np
import math
from skimage import io
from skimage.util import img_as_int
import matplotlib.pyplot as plt

# beware, this function is completely written in numpy array terms, so row = y-axis and column = x-axis
# target sizes are the sizes of the patches
def createPatchesLabeledImage(dapi_tile_path, target_row_size=128, target_column_size=128):

    #extract original dims
    image = io.imread(dapi_tile_path)
    row_size,column_size = image.shape
    empty_image = np.zeros((row_size, column_size))

    # Create patches grid
    patches_grid_size_column = int(math.floor(column_size / target_row_size * 1.0))
    patches_grid_size_row = int(math.floor(row_size / target_row_size * 1.0))
    patches_number = (patches_grid_size_column * patches_grid_size_row) 
    patches_vector = np.array(list(range(1,patches_number+1)))
    patches_vector = patches_vector.astype(int)
    patches_array = np.reshape(patches_vector, (patches_grid_size_row, patches_grid_size_column))

    # then calculate the coordinates of the extrema, sincde we math.floor the patches, there will be some unassigned. I want to assignt them to their neighbouring label, since I'd rather have them be too big than too small
    # We do this by checking if the label of the current patch is an extrema, if so, count the difference further
    extrema_column = [patches_array[row_nr,patches_grid_size_column-1] for row_nr in range(0,patches_grid_size_row)] 
    extrema_row =  [patches_array[patches_grid_size_row-1,col_nr] for col_nr in range(0,patches_grid_size_column)] 

    # these difference are how many pixels we need to count further in both dimensions
    row_difference = row_size - (patches_grid_size_row*target_row_size) # = difference on the row axis, NOT = difference of each row
    column_difference = column_size - (patches_grid_size_column*target_column_size)# = difference on the column axis, NOT = difference of each column

    # For each patch
    for row in range(0,patches_grid_size_row): # patches_grid_size_row
        for column in range(0,patches_grid_size_column): # patches_grid_size_column
            patch_label = int(patches_array[row,column])
            # first check if it is an extrema in either axis, if so, then we set the adder to the difference the image has at that axis
            column_adder = 0
            row_adder = 0
            if patch_label in extrema_column:
                column_adder = column_difference
            if patch_label in extrema_row:
                row_adder = row_difference


            # Inside each patch, for each pixel inside the patch
            for pixel_row in range(0, target_row_size+row_adder):
                for pixel_column in range(0,target_column_size+column_adder):
                    row_coordinate = pixel_row + (row * target_row_size)
                    column_coordinate = pixel_column + (column* target_column_size)
                    empty_image[row_coordinate, column_coordinate]=patch_label
    labeled_patch_image = empty_image.astype(int)
    return labeled_patch_image, patches_array

# patches_array is an ndarray of ints, as returned by createPatchesLabeledImage
def createNeighbourDict(patches_array):
    neighbourDict = {} # key = patch_label, value = list of patch labels that neighbour it
    for row in range(0,patches_array.shape[0]):
        for column in range(0,patches_array.shape[1]):
            # now we add the indexes of combination we need to make for the neighbours to a list, to be looped over later
            patch_label = str(patches_array[row, column])
            # initialize the value list for this patch label
            neighbourDict[patch_label] = []
            row_indexes = [row-1, row, row+1]
            column_indexes = [column-1, column, column+1]
            # then we loop over them and try to add their index combinations to the dictionary 
            for row_index in row_indexes:
                for column_index in column_indexes:
                    # if the current neighbour is just the label in iteration, contiue
                    if row_index == row and column_index == column:
                        continue
                    if row_index < 0 or column_index < 0:
                        continue

                    # try adding the patch labels of its neighbours, since some will be out of bounds, nothing to do about that
                    try:
                        # cast to int cause json doesn't take numpy objects
                        neighbourDict[patch_label].append(int(patches_array[row_index, column_index]))
                    except IndexError:
                        pass
    with open("patch_neighbours.json", 'w') as json_file:
        json.dump(neighbourDict, json_file)


if __name__ == "__main__":
    dapi_tile_path = "/media/tool/gabriele_data/1442_OB/maxIP-seperate-channels/DO/DAPI.tif"
    createPatchesLabeledImage(dapi_tile_path)





import os
import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def calculateTileGridStatistics(tile_grid_shape, tile_size_x: int, tile_size_y: int):
    """Calculates all necessary grid statistics based on tile shape and size

    Parameters
    ----------
    tile_grid_shape : Tuple[int, int]
        Tuple of int representing the number of tiles that fit in the x and y dimensions of the original image respectively.
    tile_size_x : int
        Number of pixels that in the x dimension of the original image 
    tile_size_y : int
        Number of pixels that in the y dimension of the original image 

    Returns
    -------
    [int] total_n_tiles
       Total number of tiles in the original image 
    [ndarray] tile_grid_array
        An array representing the layout of the tiles
    [int] original_x
        length of the original image in the x dimension
    [int] original_y
        length of the original image in the y dimension
       
    """
    total_n_tiles = tile_grid_shape[0]*tile_grid_shape[1]
    # Create range list of the tiles
    total_tiles_list = list(range(1,total_n_tiles+1))
    # Reshape the range list into the tile grid of the original image.
    # We swap the elements of the grid because the rest of the pipeline sees x and y as horizontal vs vertical, but numpy sees it as an array, where x = vertical movement
    swapped_grid = (tile_grid_shape[1],tile_grid_shape[0])
    tile_grid_array = np.reshape(total_tiles_list, swapped_grid)
    # Creating an empty array the size of an original image
    original_x = tile_grid_array.shape[1] * tile_size_x 
    original_y = tile_grid_array.shape[0] * tile_size_y
    return total_n_tiles, tile_grid_array, original_x, original_y


# This requires that the input csv had a column X and column Y
def tranformTileCoordinateSystem(path_to_csv: str, tile_grid_shape, tile_size_x, tile_size_y):
    decoded_df = pd.read_csv(path_to_csv)
    original_x_column = []
    original_y_column = []

    total_n_tiles, tile_grid_array, _, _ = calculateTileGridStatistics(tile_grid_shape, tile_size_x, tile_size_y)
    for row in decoded_df.itertuples():
        # extract X and Y coordinates of the respective tile the spot belongs to
        row_location, col_location = np.where(tile_grid_array==row.Tile) # this returns rows and columns, NOT X and Y, which is the opposite
        # unpacking the array structure of the return tuple of np.where
        y_tile_location, x_tile_location = row_location[0], col_location[0]
        # Calculate how many pixels to add in order to plot the spot in the correct tile in the original image
        x_adder = x_tile_location * tile_size_x
        y_adder = y_tile_location * tile_size_y
        # Calculate the position in the original image
        x_coordinate = row.X + x_adder
        y_coordinate = row.Y + y_adder
        original_x_column.append(x_coordinate)
        original_y_column.append(y_coordinate)
    decoded_df['Original_X'] = original_x_column
    decoded_df['Original_Y'] = original_y_column
    return decoded_df

if __name__=="__main__":
    decoded_genes = "/media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/results2/decoded/concat_decoded_genes.csv"
    tranformTileCoordinateSystem(decoded_genes, (2,2), 700,500)



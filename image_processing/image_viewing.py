import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cv2

reference = "/media/tool/starfish_test_data/ExampleInSituSequencing/DO/REF.TIF"
blobs = "/home/nacho/Documents/Code/communISS/results/blobs/concat_blobs.csv"

''' cv2 coordinate system:
0/0---X--->
 |
 |
 Y
 |
 |
 v
'''

def plotSpotsOnWholeImage(path_to_img, path_to_spotsCSV, tile_grid_shape, tile_size_x, tile_size_y, plotlib=False):
    df = pd.read_csv(path_to_spotsCSV)
    image = cv2.imread(path_to_img)
    empty_image = np.zeros(image.shape)


    # Calculate image properties:
    n_total_tiles = tile_grid_shape[0]*tile_grid_shape[1]
    total_tiles_list = list(range(1,n_total_tiles+1))
    tile_array = np.reshape(total_tiles_list, tile_grid_shape)

    for row in df.itertuples():
        row_location, col_location = np.where(tile_array==row.Tile) # this returns rows and columns, NOT X and Y, which is the opposite
        # unpacking the array structure of the return tuple of np.where
        y_tile_location, x_tile_location = row_location[0], col_location[0]
        x_adder = x_tile_location * tile_size_x 
        y_adder = y_tile_location * tile_size_y
        x_coordinate = row.X + x_adder
        y_coordinate = row.Y + y_adder
        empty_image[y_coordinate, x_coordinate]=255
    if plotlib==True:
        fig, axs = plt.subplots(1, 2)
        axs[0, 0].imshow(image)
        axs[0, 0].set_title('Original image')
        axs[0, 1].imshow(empty_image)
        axs[0, 1].set_title("Detected spots")
        for ax in axs.flat:
            ax.set(xlabel='X-coordinates', ylabel='y-coordinates')

    else:
        cv2.imshow("Original", image)
        cv2.imshow("Detected spots", empty_image)
        cv2.waitKey(0)
plotSpotsOnWholeImage(reference, blobs, (2,2), 665, 490, plotlib=True)
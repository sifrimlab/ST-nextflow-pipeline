import numpy as np
from skimage import io
import matplotlib.pyplot as plt
from matplotlib.colors import colorConverter
import pandas as pd
import cv2
from typing import Tuple
from ast import literal_eval as make_tuple

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

def legendWithoutDuplicateLabels(ax):
    """Does the same as ax.legend(), but if there are duplicate labels in the list, they are skipped.

    Parameters
    ----------
    ax : matplotlib.axes
        The axis onto which the legend is supposed to be placed.
    """
    handles, labels = ax.get_legend_handles_labels()
    unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
    ax.legend(*zip(*unique))

def plotSpotsOnWholeImage(path_to_spotsCSV: str, tile_grid_shape: Tuple[int, int], tile_size_x: int, tile_size_y: int, path_to_original_img=""):
    """Takes a csv of spots as calculated by spotDetection.py and plots them on an untiled empty canvas that has the size of the original image.

    Parameters
    ----------
    path_to_spotsCSV : str
        Path to input csv file that contains the spots. They should include the following columns, spelled as such:
        'Tile', 'X', 'Y', 'Sigma'
    tile_grid_shape : tuple
        Tuple of ints containing the x and y size of the original image (in that order). eg.: (1330, 980) 
    tile_size_x : int
        Number of columns in the tiled images, or the size of the X-axis.
    tile_size_y : int
        Number of rows in the tiled images, or the size of the Y-axis.

    path_to_img : str, optional
        Path to input image of which the spots originate
    """
    # Parse input
    df = pd.read_csv(path_to_spotsCSV)

    # Calculate tile grid properties:
    total_n_tiles, tile_grid_array, original_x, original_y = calculateTileGridStatistics(tile_grid_shape, tile_size_x, tile_size_y)
    # Create empty image size of the original image
    empty_image=np.zeros((original_y, original_x))

    if path_to_original_img:
        fig, axs = plt.subplots(1,2)
        image = cv2.imread(path_to_original_img)
        axs[0].imshow(image)
        axs[0].set_title('Original image')
        axs[1].imshow(empty_image)
        axs[1].set_title("Detected spots")
        for row in df.itertuples():
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

            circ = plt.Circle((x_coordinate, y_coordinate), radius=3)
            axs[1].add_patch(circ)
        for ax in axs:
            ax.set(xlabel='X-coordinates', ylabel='y-coordinates')
    else: 
        fig,ax = plt.subplots(1,1)
        ax.imshow(empty_image, cmap='gray')
        for row in df.itertuples():
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
            circ = plt.Circle((x_coordinate, y_coordinate), radius=2)
            ax.add_patch(circ)
        fig.tight_layout()
        plt.savefig("detected_spots_plotted.pdf")



def plotDecodedGenesOnWholeImage(path_to_original_image: str,  path_to_spotsCSV: str, tile_grid_shape: Tuple[int, int], tile_size_x: int, tile_size_y: int):
    image = io.imread(path_to_original_image)
    df = pd.read_csv(path_to_spotsCSV)
    genes_list = set(df['Gene'])
    # Making a colormap that picks a different color for each gene (and empty string)
    cmap=plt.get_cmap('gist_rainbow')
    colors = cmap(np.linspace(0, 1, len(genes_list)))
    color_dict = {gene:color for gene,color in zip(genes_list,colors)}

    ## Calculate image properties:
    total_n_tiles, tile_grid_array, original_x, original_y = calculateTileGridStatistics(tile_grid_shape, tile_size_x, tile_size_y)    
    fig, ax = plt.subplots(1,1)
    ax.imshow(image, cmap='gray')
    ax.set_title("Decoded genes")
    for row in df.itertuples():
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
        gene = row.Gene
        if str(gene) == "nan":
            ## Now we plot the dot
            circ = plt.Circle((x_coordinate, y_coordinate), radius=3, color=color_dict[gene], label=gene)
            ax.add_patch(circ)
    # legendWithoutDuplicateLabels(ax)
    fig.tight_layout()
    plt.savefig("decoded_genes_plotted.pdf")
    # plt.show()

    # Now the same with nonrecognized spots included
    fig, ax = plt.subplots(1,1)
    ax.imshow(image, cmap='gray')
    ax.set_title("Decoded genes")
    for row in df.itertuples():
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
        gene = row.Gene
        ## Now we plot the dot
        circ = plt.Circle((x_coordinate, y_coordinate), radius=3, color=color_dict[gene], label=str(gene))
        ax.add_patch(circ)
    # legendWithoutDuplicateLabels(ax)
    fig.tight_layout()
    plt.savefig("all_decoded_spots_plotted.pdf")

def plotSpotsOnTile(path_to_tile_image: str, path_to_spotsCSV: str, radius: int):
    image = io.imread(path_to_tile_image)
    df = pd.read_csv(path_to_spotsCSV)

    fig, ax = plt.subplots(1,1)
    ax.imshow(image, cmap='gray')
    ax.set_title("Detected spots")
    for row in df.itertuples():
        ## Now we plot the dot
        circ = plt.Circle((row.X, row.Y), radius=radius)
        ax.add_patch(circ)
    fig.tight_layout()
    return plt

def plotDecodedGenesOnTile(path_to_tile_image: str, path_to_decoded_spots: str, radius: int):
    image = io.imread(path_to_tile_image)
    df = pd.read_csv(path_to_decoded_spots)
    genes_list = set(df['Gene'])
    # Making a colormap that picks a different color for each gene (and empty string)
    cmap=plt.get_cmap('gist_rainbow')
    colors = cmap(np.linspace(0, 1, len(genes_list)))
    color_dict = {gene:color for gene,color in zip(genes_list,colors)}

    ## Calculate image properties:
    fig, ax = plt.subplots(1,1)
    ax.imshow(image, cmap='gray')
    ax.set_title("Decoded genes")
    for row in df.itertuples():
        gene = row.Gene
        if str(gene) != "nan":
            # Now we plot the dot
            circ = plt.Circle((row.X, row.Y), radius=3, color=color_dict[gene], label=gene)
            ax.add_patch(circ)
    # legendWithoutDuplicateLabels(ax)
    fig.tight_layout()
    return plt

    # # Now the same with nonrecognized spots included
    # fig, ax = plt.subplots(1,1)
    # ax.imshow(image, cmap='gray')
    # ax.set_title("Decoded genes")
    # for row in df.itertuples():
    #     # extract X and Y coordinates of the respective tile the spot belongs to
    #     row_location, col_location = np.where(tile_grid_array==row.Tile) # this returns rows and columns, NOT X and Y, which is the opposite
    #     # unpacking the array structure of the return tuple of np.where
    #     y_tile_location, x_tile_location = row_location[0], col_location[0]
    #     # Calculate how many pixels to add in order to plot the spot in the correct tile in the original image
    #     x_adder = x_tile_location * tile_size_x 
    #     y_adder = y_tile_location * tile_size_y
    #     # Calculate the position in the original image
    #     x_coordinate = row.X + x_adder
    #     y_coordinate = row.Y + y_adder
    #     gene = row.Gene
    #     ## Now we plot the dot
    #     circ = plt.Circle((x_coordinate, y_coordinate), radius=3, color=color_dict[gene], label=str(gene))
    #     ax.add_patch(circ)
    # # legendWithoutDuplicateLabels(ax)
    # fig.tight_layout()
    # plt.savefig("all_decoded_spots_plotted.pdf")

if __name__=='__main__':
    reference_image = "/media/tool/gabriele_data/1442_OB/maxIP-seperate-channels/DO/REF.tif"
    decoded_genes= "/media/tool/gabriele_data/1442_OB/maxIP-seperate-channels/results_minsigma2_maxsigma20/decoded/concat_decoded_genes.csv" 
    tile_grid_shape =(8,6) 
    tile_size_x = int(float(1875))
    tile_size_y = int(float(2200))
    plotDecodedGenesOnWholeImage(reference_image, decoded_genes, tile_grid_shape, tile_size_x, tile_size_y)

    # tile_image = "/media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/results/tiled_DO/REF_padded_tiled_3.tif"
    # spotsCSV = "/media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/results/blobs/REF_padded_tiled_3_filtered_blobs.csv"
    # plotSpotsOnTile(tile_image, spotsCSV, 3)



     # = "/media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/results/tiled_DO/REF_padded_tiled_3.tif"
    # decoded_genes_csv = "/media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/results/decoded/decoded_tiled_3.csv"
    # plotDecodedGenesOnTile(tile_image, decoded_genes_csv, 3)

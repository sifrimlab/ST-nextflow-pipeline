import pandas as pd
import matplotlib.pyplot as plt
from skimage import io


def plotGeneExpression(image_path: str, decoded_genes: str, barcode: int):
    img  = io.imread(image_path)
    decoded_genes= pd.read_csv(decoded_genes)
    filtered_spots = decoded_genes[decoded_genes['Barcode'] == barcode]
    fig, ax = plt.subplots(1,1)
    ax.imshow(img, cmap='gray')
    for row in filtered_spots.itertuples():
        circ = plt.Circle((row.X, row.Y), radius=2)
        ax.add_patch(circ)
    return plt




if __name__ == '__main__':
    image = "/media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/results2/tiled_DO/REF_padded_tiled_3.tif"
    decoded_genes = "/media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/results2/decoded/decoded_tiled_3.csv"
    gene_name = "5534"
    plotGeneExpression(image, decoded_genes, gene_name)

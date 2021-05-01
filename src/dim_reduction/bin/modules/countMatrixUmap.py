import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn as sk
from sklearn.preprocessing import StandardScaler
import umap

"""
    @contributions: umap code provided by Jose Ignacio Alvira Larizgoita
"""
def createAndPlotUmap(count_matrix_csv: str):
    # Read the expression data matrix 
    raw_data = pd.read_csv(count_matrix_csv)
    # format for rest should be: cells as rows and genes as columns, so we adapt the index and transpose
    raw_data_indexed = raw_data.set_index('Gene')
    raw_data_indexed = raw_data_indexed.drop(columns=['0']) # remove the column that represents assignment to background
    transposed = raw_data_indexed.transpose()

    # Log transform if you want
    log_data = transposed.astype(np.float32).apply(lambda x: np.log2(x+1), axis=1)

    # # Standardize if you want
    standardizer = StandardScaler()
    standard_data = standardizer.fit_transform(log_data)

    # Now UMAP out of the dataframe of your choice
    reducer = umap.UMAP()
    embedding = reducer.fit_transform(standard_data) #or logdata or standard data or whatever

    # Plot the ugliest plots of your life
    plt.scatter(embedding[:,0],embedding[:,1])

    return plt


if __name__=="__main__":
    count_matrix_csv = "/media/david/Puzzles/starfish_test_data/MERFISH/seperate_stacks_cropped/results_tiled_whitetophat/final/count_matrix.csv"
    plot = createAndPlotUmap(count_matrix_csv)
    plot.savefig("/media/david/Puzzles/starfish_test_data/MERFISH/seperate_stacks_cropped/results_tiled_whitetophat/final/count_matrix_umap.svg")

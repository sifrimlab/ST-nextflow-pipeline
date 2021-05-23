import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def calculateGenesLeftAfterIntensityThresholding(intensities_df, threshold: float):
    leftover = len(intensities_df[intensities_df['Intensity_ratio']>threshold])
    return leftover

def plotSpotsLeftAfterIntensityThresholding(path_to_decoded_genes: str):
    df = pd.read_csv(path_to_decoded_genes)
    mask = df.Gene.notnull()
    recognized_df = df[mask]
    unrecognized_df =df[~mask]


    fig, ax = plt.subplots(1,1)
    ax.set_title("Number of spots remaining after thresholding based on max channel intensity normalized by sum of all channel intensities")
    ax.set_xlabel("Threshold (%)")
    ax.set_ylabel("# of genes that pasthe threshold")

    x = np.linspace(0.25, 1, 100)
    y_recognized= [calculateGenesLeftAfterIntensityThresholding(recognized_df, threshold) for threshold in x]
    ax.plot(x, y_recognized, 'g-', label="recognized spots")

    x = np.linspace(0.25, 1, 100)
    y_nonrecognized= [calculateGenesLeftAfterIntensityThresholding(unrecognized_df, threshold) for threshold in x]

    # find biggest difference between x and y
    differences = {threshold:recog - nonrecog for threshold, recog, nonrecog in zip(x, y_recognized,y_nonrecognized)}
    max_index = max(differences, key=differences.get)
    max_difference = differences[max_index]

    ax.plot(x, y_nonrecognized, 'r-', label = "non-recognized spots")
    ax.axvline(max_index, color='k', label="optimal threshold")
    fig.tight_layout()

    plt.legend()
    plt.savefig("decoding_intensity_QC.svg", format="svg", dpi=1200)

# argparsing

decoded_genes = sys.argv[1]
plotSpotsLeftAfterIntensityThresholding(decoded_genes)

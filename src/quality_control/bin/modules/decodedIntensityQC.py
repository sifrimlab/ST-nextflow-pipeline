import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def calculateGenesLeftAfterIntensityThresholding(path_to_intensities: str, threshold: float):
    df = pd.read_csv(path_to_intensities)
    leftover = len(df[df['Intensity_ratio']>threshold])
    return leftover

def plotSpotsLeftAfterIntensityThresholding(path_to_intensities: str):
    x = np.linspace(0.25, 1, 100)
    y= [calculateGenesLeftAfterIntensityThresholding(path_to_intensities, threshold) for threshold in x]
    plt.plot(x, y, 'g-')
    plt.show()


    

if __name__=="__main__":
    intensities = "/media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/results2/intensities/tile3_max_intensities.csv"
    plotSpotsLeftAfterIntensityThresholding(intensities)



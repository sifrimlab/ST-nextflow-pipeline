import math
import numpy as np
import pandas as pd

path_to_spots = "concat_blobs.csv"
def filterSpotsBasedOnSigmas(spots_csv: str, num_stdev: int):
    original_array = np.genfromtxt(path_to_spots, delimiter=',', skip_header=1)
    original_array = original_array.astype(int)
    sigmas = original_array[:,3]
    average = np.mean(sigmas)
    stdev = np.std(sigmas)
    interval = (math.floor(average-stdev), math.ceil(average+stdev))
    # is_between_list = [interval[0] <= sigma <= interval[1] for sigma in sigmas]
    filtered_spots = original_array[np.logical_and(original_array[:,3] >= interval[0], original_array[:,3] < interval[1])]
     
    num_spots_filtered_out = int(len(original_array) - len(filtered_spots))

def checkSpotsInRounds(ref_spots_csv: str, round_spots_csv: str):
    ref_array = np.genfromtxt(path_to_spots, delimiter=',', skip_header=1)
    ref_array = original_array.astype(int)
    round_array = np.genfromtxt(path_to_spots, delimiter=',', skip_header=1)
    round_array = original_array.astype(int)




import math
import numpy as np
import pandas as pd

ref_spots_csv = "/media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/results/blobs/REF_padded_tiled_3_filtered_blobs.csv"
rounds_csv = [f"/media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/results/hybs/Round2_c{i}_padded_registered_tiled_3_filtered_registered_hybs.csv" for i in range (2,6)]
# print(rounds_csv)
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

# This function assumes that the given csv's are for the same tile, it does not check that beforehand
def checkSpotsInRounds(ref_spots_csv: str, round_spots_csv_list):
    # columns: 0 = tile, 1 = Y, 2=X, 3=Sigma
    ref_array = np.genfromtxt(ref_spots_csv, delimiter=',', skip_header=1)
    ref_array = ref_array.astype(int)

    # round_spots_csv_list will be a list of filepath that point towards the hybs detected on a specific channel, we want to combine those
    # columns: 0 = tile, 1=Round, 2=Channel, 3 = Y, 4=X, 5=Sigma
    channel_array_list=[]
    for channel in round_spots_csv_list:
        try:
            temp_array = np.genfromtxt(channel, delimiter=',', skip_header=1).astype(int)
            channel_array_list.append(temp_array)
        except: 
            pass

    channel_array = np.vstack(channel_array_list)

    array_of_tuples = map(tuple, arr)
    tuples = tuple(array_of_tuples)
    print(tuples) 


checkSpotsInRounds(ref_spots_csv, rounds_csv)





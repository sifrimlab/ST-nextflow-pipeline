import math
import numpy as np
import pandas as pd

ref_spots_csv = "/media/tool/gabriele_data/1442_OB/maxIP-seperate-channels/results/blobs/concat_blobs.csv"
rounds_csv = [f"/media/tool/gabriele_data/1442_OB/maxIP-seperate-channels/results/hybs/Round2_c{i}_maxIP_padded_registered_tiled_4_filtered_registered_hybs.csv" for i in range (1,5)]
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
def checkSpotsInRounds(ref_spots_csv: str, round_spots_csv_list, pixel_mismatch: int):
    # columns: 0 = tile, 1 = Y, 2=X, 3=Sigma
    ref_array = np.genfromtxt(ref_spots_csv, delimiter=',', skip_header=1)
    ref_array = ref_array.astype(int)

    # round_spots_csv_list will be a list of filepath that point towards the hybs detected on a specific channel, we want to combine those
    # columns: 0 = tile, 1=Round, 2=Channel, 3 = Y, 4=X, 5=Sigma
    channel_array_list=[]
    for channel in round_spots_csv_list:
        try:
            temp_array = np.genfromtxt(channel, delimiter=',', skip_header=1).astype(int)
            if not len(temp_array)==0:
                channel_array_list.append(temp_array)
        except: 
            pass

    # Parse ref arrays
    array_of_tuples = map(tuple, ref_array[:,(1,2)])
    ref_tuples = list(array_of_tuples)

    # Parse round arrays
    channel_array = np.vstack(channel_array_list)
    array_of_tuples = map(tuple, channel_array[:,(3,4)])
    round_tuples = list(array_of_tuples)
    # Now we have a list of tuples where each tuple is an Y,X

    # compares two tuples and sees if they are "the same", as defined by an interval of allowed pixel mismatch
    def compareTuplesValues(ref_tuple, target_tuple, pixel_mismatch: int):
        # x and y here are meaningless, only thing that's important is that the respective coordinates are in the same column for both tuples
        x_interval = (ref_tuple[0]-pixel_mismatch,ref_tuple[0]+pixel_mismatch) 
        y_interval = (ref_tuple[1]-pixel_mismatch,ref_tuple[1]+pixel_mismatch) 
        if x_interval[0] < target_tuple[0] < x_interval[1] and y_interval[0] < target_tuple[1] < y_interval[1] :
            return True
        else:
            return False

    nr_matches=0
    # x_sorted_ref_tuples = sorted(ref_tuples, key=lambda x: x[0])
    # y_sorted_ref_tuples = sorted(ref_tuples, key=lambda x: x[1])
    # x_sorted_round_tuples = sorted(round_tuples, key=lambda x: x[0])
    # y_sorted_round_tuples = sorted(round_tuples, key=lambda x: x[1])

    # this is not going to be optimized in any way, time will tell if it is necessary or not
    for ref_tuple in ref_tuples:
        for round_tuple in round_tuples:
            if compareTuplesValues(ref_tuple, round_tuple, pixel_mismatch):
                nr_matches +=1
                break
            else:
                continue
    nr_misses = len(ref_tuples) - nr_matches
    print(f"nr_matches = {nr_matches} and nr_mismatches = {nr_misses}")
                



checkSpotsInRounds(ref_spots_csv, rounds_csv, 3)


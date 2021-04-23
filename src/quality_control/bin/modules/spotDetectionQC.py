import math
from skimage import io
import matplotlib.pyplot as plt
import numpy as np

ref_spots_csv = "/media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/results/blobs/REF_normalized_padded_tiled_3_filtered_blobs.csv"
rounds_csv = [f"/media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/results/hybs/Round2_c{i}_normalized_padded_registered_tiled_3_filtered_registered_hybs.csv" for i in range (2,6)]
original_image = "/media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/results/tiled_DO/REF_normalized_padded_tiled_3.tif"

def filterSpotsBasedOnSigmas(path_to_spots: str, num_stdev=1):
    original_array = np.genfromtxt(path_to_spots, delimiter=',', skip_header=1)
    original_array = original_array.astype(int)
    sigmas = original_array[:, 3]
    average = np.mean(sigmas)
    stdev = np.std(sigmas)
    interval = (math.floor(average-(stdev*num_stdev)), math.ceil(average+(stdev*num_stdev)))
    filtered_spots = original_array[np.logical_and(original_array[:,3] >= interval[0], original_array[:,3] < interval[1])]
    num_spots_filtered_out = int(len(original_array) - len(filtered_spots))

# This function assumes that the given csv's are for the same tile, it does not check that beforehand
def checkSpotsInRounds(ref_spots_csv: str, round_spots_csv_list, original_image, pixel_mismatch: int):
    original_image = io.imread(original_image)
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
    def calculateEuclideanDistance2D(ref_tuple, target_tuple):
        dist = math.sqrt((ref_tuple[0] - target_tuple[0])**2+(ref_tuple[1]-target_tuple[1])**2)
        return dist
    def compareTuplesValues(ref_tuple, target_tuple, pixel_mismatch: int):
        # x and y here are meaningless, only thing that's important is that the respective coordinates are in the same column for both tuples
        x_interval = (ref_tuple[0]-pixel_mismatch,ref_tuple[0]+pixel_mismatch)
        y_interval = (ref_tuple[1]-pixel_mismatch,ref_tuple[1]+pixel_mismatch)
        if x_interval[0] < target_tuple[0] < x_interval[1] and y_interval[0] < target_tuple[1] < y_interval[1] :
            return True
        else:
            return False

    # x_sorted_ref_tuples = sorted(ref_tuples, key=lambda x: x[0])
    # y_sorted_ref_tuples = sorted(ref_tuples, key=lambda x: x[1])
    # x_sorted_round_tuples = sorted(round_tuples, key=lambda x: x[0])
    # y_sorted_round_tuples = sorted(round_tuples, key=lambda x: x[1])

    # this is not going to be optimized in any way, time will tell if it is necessary or not
    closest_point_dict = {}
    for ref_tuple in ref_tuples:
        # min returns the original iterable, not the result of the key function
        closest_point = min(round_tuples, key=lambda x: calculateEuclideanDistance2D(ref_tuple, x))
        closest_point_dict[ref_tuple] = closest_point

    fig, axs = plt.subplots(1,2)
    axs[0].imshow(original_image, cmap='gray')
    axs[0].set_title("Reference")
    axs[1].imshow(original_image, cmap='gray')
    axs[1].set_title("Round")
    for key, value in closest_point_dict.items():
        # key & value in format: (Y,X)
        color=np.random.rand(1,3)
        circ1 = plt.Circle((key[1],key[0]), 2, color=color)
        circ2 = plt.Circle((value[1],value[0]), 2, color=color)
        axs[0].add_patch(circ1)
        axs[1].add_patch(circ2)
    plt.show()

    # nr_misses = len(ref_tuples) - nr_matches
    # print(f"nr_matches = {nr_matches} and nr_mismatches = {nr_misses}")
if __name__=='__main__':
    checkSpotsInRounds(ref_spots_csv, rounds_csv, original_image, 2)


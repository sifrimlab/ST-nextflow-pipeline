import math
from collections import Counter
from skimage import io
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json

# compares two tuples and sees if they are "the same", as defined by an interval of allowed pixel mismatch
def compareTuplesValues(ref_tuple, target_tuple, pixel_mismatch: int):
    # x and y here are meaningless, only thing that's important is that the respective coordinates are in the same column for both tuples
    x_interval = (ref_tuple[0]-pixel_mismatch,ref_tuple[0]+pixel_mismatch)
    y_interval = (ref_tuple[1]-pixel_mismatch,ref_tuple[1]+pixel_mismatch)
    if x_interval[0] < target_tuple[0] < x_interval[1] and y_interval[0] < target_tuple[1] < y_interval[1] :
        return True
    else:
        return False
# Define euclidean distance between a tuple
def calculateEuclideanDistance2D(ref_tuple, target_tuple):
    dist = math.sqrt((ref_tuple[0] - target_tuple[0])**2+(ref_tuple[1]-target_tuple[1])**2)
    return dist

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
def checkSpotsInRoundPrecision(ref_spots_csv: str, round_spots_csv_list, round_nr, pixel_distance= 0, x_column_name="X", y_column_name="Y",original_image=""):
    ref_spots_df = pd.read_csv(ref_spots_csv)
    #Extract only relevant columns X and Y
    ref_spots_df = ref_spots_df[[x_column_name, y_column_name]]
    # From now on consistency is important: everything in this function will assume that X is the first column of the np array, and Y is the second
    ref_array = ref_spots_df.to_numpy()
    # cast to int for insurance, shouldn't be necessary though
    ref_array = ref_array.astype(int)

    # round_spots_csv_list will be a list of filepath that point towards the hybs detected on a specific channel, we want to combine those
    round_array_list=[] # name is out of date, since it'll also take each tile
    for csv_file in round_spots_csv_list:
        try:
            temp_df = pd.read_csv(csv_file)
            temp_df = temp_df[[x_column_name, y_column_name]]
            temp_array = temp_df.to_numpy()
            temp_array = temp_array.astype(int)
            # If one of the spot detected lists is empty, it shouldn't be included
            if not len(temp_array)==0:
                round_array_list.append(temp_array)
        except:
            pass
    # Parse ref arrays
    array_of_tuples = map(tuple, ref_array) # convert array to tuples
    ref_tuples = list(array_of_tuples)

    # Parse round arrays
    try:
        round_array = np.vstack(round_array_list)
    # It could be that this tile doesn't actually contain any spots, in that case return should be empty
    except ValueError:
        return

    array_of_tuples = map(tuple, round_array) #convert arrays to tuples
    round_tuples = list(array_of_tuples)
    # Now we have a list of tuples where each tuple is an Y,X

    # this is not going to be optimized in any way, time will tell if it is necessary or not
    all_closest_ref_point_dict = {} # key = spot in round, value = spot in reference
    all_closest_distance_dict = {}  # key = spot in round, value = distance to closest ref spot
    closest_ref_point_dict = {} # key = spot in round, value = spot in reference
    closest_distance_dict = {}  # key = spot in round, value = distance to closest ref spot
    for round_tuple in round_tuples:
        # min returns the original iterable, not the result of the key function
        try:
            closest_ref_point = min(ref_tuples, key=lambda x: calculateEuclideanDistance2D(round_tuple, x))
            closest_distance =  calculateEuclideanDistance2D(round_tuple, closest_ref_point)
            all_closest_ref_point_dict[round_tuple] = closest_ref_point
            all_closest_distance_dict[round_tuple] = closest_distance
            if closest_distance <= pixel_distance:
                # print(f"round_tuple = {round_tuple}, closest_ref_tuple = {closest_ref_point}, with distance = {closest_distance}")
                closest_ref_point_dict[str(round_tuple)] = str(closest_ref_point)
                closest_distance_dict[str(round_tuple)] = closest_distance
        # If there are no spots in the ref image, this needs to be excepted
        # Then this point will also not be added, so end result is the same
        except ValueError:
            pass

    # create the table of info
    attribute_dict = {}
    nr_matched_spots =  len(closest_ref_point_dict)
    nr_round_spots_total = len(all_closest_ref_point_dict)
    nr_unmatched_spots = nr_round_spots_total - len(closest_ref_point_dict)
    attribute_dict['Round #'] = round_nr
    attribute_dict['# matched spots'] = nr_matched_spots
    attribute_dict['# unmatched spots'] = nr_unmatched_spots
    attribute_dict['Total Spots'] = nr_round_spots_total

    try: # if no spots were found in the round, then this will divide by zero
        attribute_dict['Ratio of matched spots'] = round(nr_matched_spots / nr_round_spots_total, 3)*100
    except ZeroDivisionError:
        attribute_dict['Ratio of matched spots'] = 0


    # if original_image:
    #     # read in image, pure for plotting purposes
    #     original_image = io.imread(original_image)
    #     _ , axs = plt.subplots(1,2)
    #     axs[0].imshow(original_image, cmap='gray')
    #     axs[0].set_title("Reference")
    #     axs[1].imshow(original_image, cmap='gray')
    #     axs[1].set_title("Round")
    #     for key, value in closest_ref_point_dict.items():
    #         # key & value in format: (Y,X)
    #         color=np.random.rand(3,)
    #         circ1 = plt.Circle((key[1],key[0]), 2, color=color)
    #         circ2 = plt.Circle((value[1],value[0]), 2, color=color)
    #         axs[0].add_patch(circ1)
    #         axs[1].add_patch(circ2)

        # Plot duplicate assignement counted
        # _, axs = plt.subplots(1,1)
        # axs.set_title("Multiple assigned reference spots plotted by counts")
        # axs.set_xlabel("# round spots a reference spot is assigned to")
        # axs.set_ylabel("# times counted")
        # closest_ref_points = closest_ref_point_dict.values()
        # counted_dict = Counter(closest_ref_points)
        # duplicate_ref_point_dict ={k: v for k, v in counted_dict.items() if v > 1}
        # axs.hist(duplicate_ref_point_dict.values())
        # for rect in axs.patches:
        #     height = rect.get_height()
        #     axs.annotate(f'{int(height)}', xy=(rect.get_x()+rect.get_width()/2, height),
        #                  xytext=(0, 5), textcoords='offset points', ha='center', va='bottom')
        # plt.show()
    return closest_ref_point_dict, attribute_dict

def calculateRecall(ref_spots_csv, dict_of_closest_ref_point_dicts, x_column_name="X", y_column_name="Y"):
    ref_spots_df = pd.read_csv(ref_spots_csv)
    #Extract only relevant columns X and Y
    ref_spots_df = ref_spots_df[[x_column_name, y_column_name]]
    # From now on consistency is important: everything in this function will assume that X is the first column of the np array, and Y is the second
    ref_array = ref_spots_df.to_numpy()
    # cast to int for insurance, shouldn't be necessary though
    ref_array = ref_array.astype(int)

    array_of_tuples = map(tuple, ref_array) # convert array to tuples
    ref_tuples = list(array_of_tuples)

    #dict_of_closest_ref_point_dicts is supposed to contain key=int(round_number), value = closest_ref_point_dicts created by checkSpotsInRoundPrecision
    #Make a list of the keys (= round numbers) and sort them, such that searching in the dict is targeted and not iterated, to ensure correct order.
    round_numbers =list(dict_of_closest_ref_point_dicts.keys())
    round_numbers.sort(key=lambda x: int(x))

    #Then iterate over each tuple in the ref_tuples, check if it's present in the values() of each round. Log when this stops being the case
    complete_barcodes = [] #If a spot ends up having a complete barcode, add it to this list
    round_not_found = {} # key = round_nr, value = count of how many barcodes did not find a match in the given round
    for ref_tuple in ref_tuples:
        ref_tuple = str(ref_tuple)
        for round_nr in round_numbers:
            matched_ref_points = dict_of_closest_ref_point_dicts[round_nr].values()
            if ref_tuple not in matched_ref_points:
                round_not_found[round_nr]= round_not_found.get(round_nr, 0) + 1
                break
            # If this level is reached, that means that for this spot, there was no round where it wasn't found, meaning that it's a complete barcode
            complete_barcodes.append(ref_tuple)

    # Duplicates may be present since a several round spots can be assigned to the same ref spot
    complete_barcodes =list(set(complete_barcodes))
    # Calculate how many spots ended up being complete barcodes
    nr_complete = len(complete_barcodes)
    nr_total = len(ref_tuples)
    nr_incomplete = nr_total - nr_complete
    try:
        ratio_complete = round(nr_complete / nr_total, 3)*100
    except ZeroDivisionError: # If number total = 0, this'll throw a ZeroDivisionError
        ratio_complete = 0

    attribute_dict = {}
    attribute_dict["spots on ref"] = nr_total
    attribute_dict["Complete barcodes"] = nr_complete
    attribute_dict["incomplete barcodes"] = nr_incomplete
    attribute_dict["Ratio Complete Barcodes"] = ratio_complete


    # Now we make a plot out of at which round  the complete barcode stops
    lists = sorted(round_not_found.items()) # sorted by key, return a list of tuples
    #unzip the list of tuples into x and y
    lists = [[ i for i, j in lists ],
          [ j for i, j in lists ]]
    x = lists[0]
    x_labels = [f"Round {int(i)}" for i in x]

    y = lists[1]

    # parse y into being a a negatice cumcount, not just absolute values
    spots_left = nr_total
    for i, y_el in enumerate(y):
        spots_left = spots_left - y_el
        y[i] = spots_left

    _, ax = plt.subplots(1,1)
    ax.bar(x,y, color="maroon")
    for rect in ax.patches:
        height = rect.get_height()
        ax.annotate(f'{int(height)}', xy=(rect.get_x()+rect.get_width()/2, height),
                    xytext=(0, 5), textcoords='offset points', ha='center', va='bottom')
    ax.plot(x,y, "o-k")
    ax.set_title(f"Potential complete barcodes left out of the {nr_total} spots after reach round")
    ax.set_ylabel("Number of potential complete barcodes remaining")
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, rotation= 45)

    return attribute_dict, round_not_found, plt




def spotDetectionQCWorkflow(ref_spots_csv, round_csv_dict):
    dict_of_closest_ref_point_dicts= {}
    rows_list = []
    for round_nr,hyb_list in rounds_csv_dict.items():
        try:
            closest_ref_point_dict, attribute_dict = checkSpotsInRoundPrecision(ref_spots_csv, hyb_list, round_nr, pixel_distance=3)
            dict_of_closest_ref_point_dicts[round_nr] = closest_ref_point_dict
            rows_list.append(attribute_dict)
        # If no spot are found, it will try to unpack null, which needs to be excepted
        # and then the function needs to exit, since without spots on a certain round, no complete barcode will be found
        except TypeError:
            pass
            # print(f"No spots were detected round {round_nr}, so a complete barcode cannot be found")
            # return
    precision_df = pd.DataFrame(rows_list)
    precision_df.to_html("round_spot_detection_precision.html", index=False)

    # Build next dataframe
    rows_list=[]
    attribute_dict = calculateRecall(ref_spots_csv, dict_of_closest_ref_point_dicts)
    rows_list.append(attribute_dict)

    recall_df = pd.DataFrame(rows_list)
    recall_df.to_html("reference_spot_recall.html", index=False)


# implemented in a dumb way: just calculate complete barcodes again, but with the ref list being only those that were inside the decoded genes
def checkCompleteBarcodeDecodingRatio(decoded_genes, dict_of_closest_ref_point_dicts, nr_rounds):
    decoded_genes = pd.read_csv(decoded_genes)
    decoded_genes = decoded_genes[decoded_genes['Gene'].isnull()!=True]
    decoded_complete_barcodes = 0
    times_broken = 0
    # (dict_of_closest_ref_point_dicts[1][5]) = file
    counter = 0

    for row in tqdm(decoded_genes.itertuples()):
        # create a string tuple for X and Y
        row_tuple = f"({row.X}, {row.Y})"
        tile_nr = row.Tile
        for round_nr in range(1,nr_rounds+1):
            with open(dict_of_closest_ref_point_dicts[round_nr][tile_nr], 'r') as json_file:
                data = json.load(json_file)
                ref_points_in_this_round =list(data.values())
                if row_tuple in ref_points_in_this_round:
                    if round_nr == 5:
                        decoded_complete_barcodes+=1
                else:
                    times_broken+=1
                    break

        # print(f"decoded_complete_barcodes = {decoded_complete_barcodes}, times_broken = {times_broken}, round_reached = {round_nr}")

    with open("normal_pixel_distance_3.txt", "w") as file:
        file.write(f"decoded_complete_barcodes = {decoded_complete_barcodes}, times_broken = {times_broken}, adds up to {decoded_complete_barcodes + times_broken}, decoded genes length= {len(decoded_genes)}")


    # total_n_tiles, tile_grid_array, _, _ = calculateTileGridStatistics(tile_grid_shape, tile_size_x, tile_size_y)









if __name__=='__main__':
    # ref_spots_csv = "/media/Puzzles/gabriele_data/1442_OB/results_correct_codebook_whiteDisk3_minSigma2_maxSigma20_noNorm_stardistSegmentation_voronoiAssigned_spotDetectionQC/blobs/transformed_concat_blobs.csv"
    # # rounds_csv_dict = [f"/media/Puzzles/starfish_test_data/ExampleInSituSequencing/results_minsigma1_maxsigma2_filter3_hybDetection_thresholdSegmentation_voronoiAssignment/hybs/Round{round_nr}_c{i}_padded_registered_tiled_3_filtered_registered_hybs.csv" for i in range(2,6)]
    # rounds_csv_dict={}
    # for round_nr in range(1,5):
    #     rounds_csv_dict[round_nr] = []
    #         # for tile_nr in range(1,5):
    #     for i in range(1,5):
    #         for tile_nr in range(1,49):
    #             rounds_csv_dict[round_nr].append(f"/media/Puzzles/gabriele_data/1442_OB/results_correct_codebook_whiteDisk3_minSigma2_maxSigma20_noNorm_stardistSegmentation_voronoiAssigned_spotDetectionQC/final/Round{round_nr}_c{i}_maxIP_padded_registered_tiled_{tile_nr}_filtered_registered_hybs_transformed.csv")
    # spotDetectionQCWorkflow(ref_spots_csv, rounds_csv_dict)

    decoded_genes = "/media/Puzzles/gabriele_data/1442_OB/results_correct_codebook_whiteDisk3_minSigma2_maxSigma20_noNorm_stardistSegmentation_voronoiAssigned_spotDetectionQC/final/concat_decoded_genes_transformed.csv"
    dict_of_closest_ref_point_dicts = {}
    for round_nr in range(1,6):
        dict_of_closest_ref_point_dicts[round_nr] ={}
        for tile_nr in range(1,49):
            dict_of_closest_ref_point_dicts[round_nr][tile_nr] =f"/media/Puzzles/gabriele_data/1442_OB/results_correct_codebook_whiteDisk3_minSigma2_maxSigma20_noNorm_stardistSegmentation_voronoiAssigned_spotDetectionQC/quality_control_pixel_distance_3/spot_detection_QC/precision/tile{tile_nr}_Round{round_nr}_closest_ref_point_dict.json"
    checkCompleteBarcodeDecodingRatio(decoded_genes, dict_of_closest_ref_point_dicts, 5)

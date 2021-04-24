import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plotDecodingPotential(decoded_genes: str, codebook: str): 
    decoded_genes = pd.read_csv(decoded_genes)
    codebook = pd.read_csv(codebook)

    # First extracts all possible "good" barcodes
    true_barcode_list = [str(i) for i in list(codebook['Barcode'])]

    # extract called barcodesk
    called_barcodes_list = [str(i) for i in list(decoded_genes['Barcode'])]
    total_nr_called_spots = len(called_barcodes_list)
    # This function assumes that the length of the future barcode list elements are the same length as the inputted barcode barcode_excerpt
    intervals = range(1, len(true_barcode_list[0])+1)
    # key = length of the intermediate barcode, value = list of barcodes of that length
    sliced_barcode_dict = {str(n_rounds): [barcode[:n_rounds] for barcode in true_barcode_list] for n_rounds in intervals}

    nr_future_matches_dict = {} # key = len of the barcode, value = number of spots that still represent a future possible barcodes
    for n_rounds in intervals:
        for spot in called_barcodes_list:
            barcode_excerpt = spot[:n_rounds]
            if barcode_excerpt in sliced_barcode_dict[str(n_rounds)]:
                nr_future_matches_dict[n_rounds] = nr_future_matches_dict.get(n_rounds, 0) + 1

    ratio_future_matches_dict = {k:round((v/total_nr_called_spots), 3)*100 for k,v in nr_future_matches_dict.items()}

    # Make a pretty plot out of it
    fig, ax = plt.subplots(1,1)
    ax.set_title("Measurement of possible true barcode matches by round progression")
    ax.set_xlabel("Round number")
    ax.set_ylabel("Ratio of valid barcodes (%)")
    ax.plot(ratio_future_matches_dict.keys(), ratio_future_matches_dict.values(), '-o')
    ax.set_xticks(list(ratio_future_matches_dict.keys()))
    for x,y in zip(ratio_future_matches_dict.keys(), ratio_future_matches_dict.values()):

        label = "{:.2f}".format(y)

        plt.annotate(label, # this is the text
                     (x,y), # this is the point to label
                     textcoords="offset points", # how to position the text
                     xytext=(0,10), # distance from text to points (x,y)
                     ha='center')
    fig.tight_layout()
    return plt

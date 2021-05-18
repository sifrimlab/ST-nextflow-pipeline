import math
import pandas as pd
import matplotlib.pyplot as plt
import skimage.io
import numpy as np
import itertools
import time

def measureTime(func):
    def wrapper(*args, **kwargs):
        starttime = time.perf_counter()
        temp = func(*args, **kwargs)
        endtime = time.perf_counter()
        print(f"Time needed to run {func.__name__}: {endtime - starttime} seconds")
        return(temp)
    return wrapper


# Create a subclass to lists to make them mutable, barcodes will be cast to this class, allowing easy indexing and changing their entries 
class CharList(list):

    #constructor
    def __init__(self, s):
        list.__init__(self, s)

    #if you wnat the string as a list
    @property
    def list(self):
        return list(self)

    #if you want the string as a string, this will usually be the case
    @property
    def string(self):
        return "".join(self)

    # add a check to the original indexing method
    def __setitem__(self, key, value):
        if isinstance(key, int) and len(value) != 1:
            cls = type(self).__name__
            raise ValueError("attempt to assign sequence of size {} to {} item of size 1".format(len(value), cls))
        super(CharList, self).__setitem__(key, value)

    # adapt toSTring() behaviour
    def __str__(self):
        return self.string

    # adapt representation for transparancy
    def __repr__(self):
        cls = type(self).__name__
        return "{}(\'{}\')".format(cls, self.string)


def testChangeOfChannels(decoded_genes: str, codebook: str, permutation, nr_channels):
    # This will be implemented with str.replace()
    decoded_genes = pd.read_csv(decoded_genes)
    codebook = pd.read_csv(codebook)
    # Cast the barcodes of the codebook to charlists, they will be mutated
    codebook_barcodes = [str(entry) for entry in list(codebook['Barcode'])]
    # store called barcodees as mutable strings, since changing rounds changes the called barcodes
    called_barcodes = [str(entry) for entry in list(decoded_genes['Barcode'])]

    # Convert both permutations to strings for the replace function later
    original_permutation = [str(entry) for entry in range(1,nr_channels+1)]
    permutation = [str(entry) for entry in permutation]
    # Create conversion dict that represents which channel needs to be changed into a different channel: key= original value, value = change to which channel
    conversion_dict = {key: value for key,value in zip(original_permutation, permutation)}


    # Mutate the barcodes from the codebook to refrect the input change of channels
    for barcode in called_barcodes:
        for k,v in conversion_dict.items():
            # Replace the barcode entries by a different one, determined by the permutation
            barcode = barcode.replace(k, v)

    # # cast barcodes back to actual strings, not charlists
    # barcodes_strings = [barcode.string for barcode in barcodes]

    # Check if it did anything
    nr_matched = 0
    nr_unmatched = 0
    for barcode in called_barcodes:
        if barcode in codebook_barcodes:
            nr_matched +=1
        else:
            nr_unmatched +=1
    ratio_matched = round((nr_matched/len(called_barcodes)), 3) * 100

    return nr_matched, nr_unmatched, ratio_matched


def testChangeOfRounds(decoded_genes: str, codebook: str, permutation):
    decoded_genes = pd.read_csv(decoded_genes)
    codebook = pd.read_csv(codebook)
    # Cast the barcodes of the codebook to charlists, they will be mutated
    codebook_barcodes = [CharList(str(entry)) for entry in list(codebook['Barcode'])]
    called_barcodes = [str(entry) for entry in list(decoded_genes['Barcode'])]

    for barcode in codebook_barcodes:
        # First we store the original values
        original_values = {}
        for i, entry in enumerate(barcode):
            original_values[i] = barcode[i]
        # Then we iterate over each entry of the permutation, and mutate the barcode's value to the new index of the original barcode
        for original_i, new_index in enumerate(permutation, 0):
            new_index_value = original_values[new_index]
            barcode[original_i] = str(new_index_value)

    nr_matched = 0
    nr_unmatched = 0
    # cast barcodes back to actual strings, not charlists
    codebook_barcodes_strings = [barcode.string for barcode in codebook_barcodes]
    for barcode in called_barcodes:
        if barcode in codebook_barcodes_strings:
            nr_matched +=1
        else:
            nr_unmatched +=1
    ratio_matched = round((nr_matched/len(called_barcodes)), 3) * 100

    return nr_matched, nr_unmatched, ratio_matched

@measureTime
def testChangeOfAllChannels(decoded_genes, codebook, nr_channels):
    # Create permutations that represent switches of channels, so will be the length of the number of channels, not the length of the barcodes
    # This implementation of perumation makes sure that each channel is only converted to once, so what this does not check is if a channel is duplicated or overwritten, it only checks interchanges
    permutations = list(itertools.permutations(range(1,nr_channels+1), nr_channels))
    ratio_dict = {}
    for permutation in permutations:
        nr_matched, nr_unmatched, ratio_matched = testChangeOfChannels(decoded_genes, codebook, permutation, nr_channels)
        # if its the original permuation, add it to a variable indpeendent of the dict
        if list(permutation) == list(range(0,nr_rounds)):
            original_ratio = ratio_matched
        else:
            ratio_dict[permutation] = ratio_matched
        print(permutation,ratio_matched)

    # max_permutation = max(ratio_dict, key=ratio_dict.get)
    # max_ratio = ratio_dict[max_permutation]
    # return max_permutation, max_ratio#, ratio_dict

def testChangeOfAllRounds(decoded_genes, codebook, nr_rounds):
    permutations = list(itertools.permutations(range(nr_rounds), nr_rounds))
    ratio_dict = {}
    for permutation in permutations:
        nr_matched, nr_unmatched, ratio_matched = testChangeOfRounds(decoded_genes, codebook, permutation)
        # if its the original permuation, add it to a variable indpeendent of the dict
        if list(permutation) == list(range(0,nr_rounds)):
            original_ratio = ratio_matched
        else:
            ratio_dict[permutation] = ratio_matched

    max_permutation = max(ratio_dict, key=ratio_dict.get)
    max_permutation_ratio = ratio_dict[max_permutation]
    return max_permutation, max_permutation_ratio, original_ratio#, ratio_dict




if __name__=="__main__":
    decoded_genes= "/media/nacho/Puzzles/starfish_test_data/ExampleInSituSequencing/results2/decoded/concat_decoded_genes.csv"
    # decoded_genes= "/media/Puzzles/gabriele_data/hippo_3/results_minsigma3_maxsigma5/decoded/concat_decoded_genes.csv"
    # decoded_genes= "/media/Puzzles/gabriele_data/hippo_3/results_minsigma3_maxsigma5/decoded/concat_decoded_genes.csv"
    codebook = "/media/nacho/Puzzles/starfish_test_data/ExampleInSituSequencing/codebook_wrong.csv"
    # codebook = "/media/Puzzles/gabriele_data/hippo_3/codebook_fixed.csv"
    # codebook = "/media/Puzzles/gabriele_data/1442_OB/codebook_fixed.csv"
    nr_rounds = 5
    nr_channels = 4
    # print(testChangeOfRounds(decoded_genes, codebook, [(2,3)]))
    # print(testChangeOfChannels(decoded_genes, codebook, (2,3)))
    testChangeOfAllChannels(decoded_genes, codebook, nr_channels)
    # print(testChangeOfAllRounds(decoded_genes, codebook, nr_rounds))




    # init_string = "5543"
    # print(init_string.replace("5","1"))
    # init_string_list = []
    # init_string_list.append(init_string)
    # c = CharList(init_string)
    # c[0] = "4"
    # print(c.string)
    # print(c.string in init_string_list)


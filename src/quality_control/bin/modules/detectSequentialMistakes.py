import math
import pandas as pd
import matplotlib.pyplot as plt
import skimage.io
import numpy as np
import itertools


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


def testChangeOfChannels(decoded_genes: str, codebook: str, tuple_channel_indexes_to_change):
    decoded_genes = pd.read_csv(decoded_genes)
    codebook = pd.read_csv(codebook)
    # Cast the barcodes of the codeebook do charlists, they will be mutated
    barcodes = [CharList(str(entry)) for entry in list(codebook['Barcode'])]
    called_barcodes = [str(entry) for entry in list(decoded_genes['Barcode'])]
    first_index, second_index = tuple_channel_indexes_to_change

    # mutate the barcodes from the codebook to refrect the input change of channels
    for barcode in barcodes:
        first_index_value = barcode[first_index]
        second_index_value = barcode[second_index]
        barcode[first_index] = second_index_value
        barcode[second_index] = first_index_value

    # cast barcodes back to actual strings, not charlists
    barcodes_strings = [barcode.string for barcode in barcodes]

    # Check if it did anything
    nr_matched = 0
    nr_unmatched = 0
    for barcode in called_barcodes:
        if barcode in barcodes_strings:
            nr_matched +=1
        else:
            nr_unmatched +=1
    ratio_matched = round((nr_matched/len(called_barcodes)), 3) * 100

    return nr_matched, nr_unmatched, ratio_matched


def testChangeOfRounds(decoded_genes: str, codebook: str, tuple_round_indexes_to_change):
    decoded_genes = pd.read_csv(decoded_genes)
    codebook = pd.read_csv(codebook)
    barcodes = [str(entry) for entry in list(codebook['Barcode'])]
    called_barcodes = [CharList(str(entry)) for entry in list(decoded_genes['Barcode'])]
    first_index, second_index = tuple_round_indexes_to_change


    for barcode in called_barcodes:
        first_index_value = barcode[first_index]
        second_index_value = barcode[second_index]
        barcode[first_index] = second_index_value
        barcode[second_index] = first_index_value

    nr_matched = 0
    nr_unmatched = 0
    for barcode in called_barcodes:
        if barcode.string in barcodes:
            nr_matched +=1
        else:
            nr_unmatched +=1
    ratio_matched = round((nr_matched/len(called_barcodes)), 3) * 100

    return nr_matched, nr_unmatched, ratio_matched

def testChangeOfAllChannels(decoded_genes, codebook, nr_channels):
    permutations = list(itertools.permutations(range(nr_channels), 2))
    ratio_dict = {}
    for permutation in permutations:
        nr_matched, nr_unmatched, ratio_matched = testChangeOfChannels(decoded_genes, codebook, permutation)
        ratio_dict[permutation] = ratio_matched
        print(permutation,ratio_matched)

    max_permutation = max(ratio_dict, key=ratio_dict.get)
    max_ratio = ratio_dict[max_permutation]
    return max_permutation, max_ratio#, ratio_dict

def testChangeOfAllRounds(decoded_genes, codebook, nr_rounds):
    permutations = list(itertools.combinations(range(nr_rounds), 2))
    ratio_dict = {}
    for permutation in permutations:
        nr_matched, nr_unmatched, ratio_matched = testChangeOfRounds(decoded_genes, codebook, permutation)
        ratio_dict[permutation] = ratio_matched
        print(permutation,ratio_matched)

    max_permutation = max(ratio_dict, key=ratio_dict.get)
    max_ratio = ratio_dict[max_permutation]
    return max_permutation, max_ratio#, ratio_dict




if __name__=="__main__":
    decoded_genes= "/media/Puzzles/starfish_test_data/ExampleInSituSequencing/results2/decoded/concat_decoded_genes.csv" 
    # decoded_genes= "/media/Puzzles/gabriele_data/1442_OB/results_correct_codebook_whiteDisk3_minSigma2_maxSigma20_noNorm_stardistSegmentation_voronoiAssigned/decoded/concat_decoded_genes.csv" 
    codebook = "/media/Puzzles/starfish_test_data/ExampleInSituSequencing/codebook_wrong.csv"
    # codebook = "/media/Puzzles/gabriele_data/1442_OB/codebook_fixed.csv"
    nr_rounds = 4
    nr_channels = 4
    # testChangeOfRounds(decoded_genes, codebook, (0,1))
    # print(testChangeOfChannels(decoded_genes, codebook, (2,3)))
    # testChangeOfAllChannels(decoded_genes, codebook, nr_channels)
    testChangeOfAllRounds(decoded_genes, codebook, nr_rounds)


    # init_string = "5543"
    # init_string_list = []
    # init_string_list.append(init_string)
    # c = CharList(init_string)
    # c[0] = "4"
    # print(c.string)
    # print(c.string in init_string_list)


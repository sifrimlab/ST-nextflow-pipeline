import pandas as pd
import os
import csv
from icecream import ic


def convertLettersToNumbers(path_to_codebook: str, path_to_conversion_index: str, outfile, index_to_keep=0):
    codebook = pd.read_csv(path_to_codebook, header=None, sep=",")
    with open(path_to_conversion_index, mode='r') as file:
        reader = csv.reader(file)
        # new dict where key= numbers, values = letters
        index_dict = {rows[0]:rows[1] for rows in reader}
    copy_barcode_list = list(codebook[0])
    gene_list=list(codebook[1])
    parsed_list = []
    for element in copy_barcode_list:
        for number, letter in index_dict.items():
          element = element.replace(letter, number)
        parsed_list.append(element)
    new_dict = pd.DataFrame({ 'Barcode':parsed_list, 'Gene':gene_list })
    new_dict.to_csv(outfile)


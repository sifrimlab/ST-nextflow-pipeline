import pandas as pd
import sys
import csv

# Create empty dict
gene_dict = {}
# First we parse the codebook into a usable dict
with open("/media/tool/starfish_test_data/ExampleInSituSequencing/codebook.csv", 'r') as csvfile:

    # Check if the csv file has a header
    sniffer = csv.Sniffer()
    has_header = sniffer.has_header(csvfile.read(2048))
    csvfile.seek(0)
    if has_header:
        reader = csv.DictReader(csvfile)
        for row in reader:
            gene_dict[row['Gene']] = row['Barcode']
        for line in csvfile:
            split_line = line.split(',')
            gene_dict[split_line[0]]=split_line[1].strip()

import os 
import pandas as pd
from tabulate import tabulate
from icecream import ic
import matplotlib.pyplot as plt
import sys

def countChannelsInBarcodeList(path_to_decoded_genes: str):
    df = pd.read_csv(path_to_decoded_genes)

    barcodes = list(df['Barcode'])
    # resulting df will have the following columns:
    # 'Channel' 'Round' 'total channel count'
    total_channel_counts= {}
    channel_dict = {} # takes tuples of round/channel as 
    for element in barcodes:
        element_list = [int(digit) for digit in str(element)]
        for i,channel_nr in enumerate(element_list):
            round_nr = i+1 # Because enumerating starts with 0
            # increment the tuple combination fo round/channel with one
            channel_dict[(round_nr,channel_nr)] = channel_dict.get((round_nr,channel_nr), 0) + 1
            total_channel_counts[channel_nr] = total_channel_counts.get(channel_nr, 0) + 1

    rows_list = []
    col_names = ['round_nr', 'channel_nr', 'count']
    #grouped_by_channel_dict = {}
    for k,count in channel_dict.items():
        temp_dict = {}
        round_nr, channel_nr = k
        row_values = [round_nr, channel_nr, count]
        temp_dict = {col_names[i]: row_values[i] for i in range(0,len(col_names)) }
        rows_list.append(temp_dict)
    count_df = pd.DataFrame(rows_list)
    wide_df = count_df.pivot_table(index=["channel_nr"], columns='round_nr', values='count', margins=True, aggfunc='sum')
    wide_df.to_csv("channels_called.csv")
def evaluateRandomCalling(path_to_decoded_genes: str, path_to_codebook: str, ratio_recognized_barcodes: int = 0):
    codebook_df = pd.read_csv(path_to_codebook)
    decoded_df = pd.read_csv(path_to_decoded_genes)
    n_genes_to_find=len(codebook_df)
    n_spots= len(decoded_df)
    decoded_df['Counted'] = decoded_df.groupby('Barcode')['Gene'].transform('size')
    unique_df = decoded_df[['Barcode', 'Counted']].drop_duplicates()
    n_unique_barcodes_called = len(unique_df)



def countRecognizedBarcodeStats(path_to_decoded_genes: str):
    df = pd.read_csv(path_to_decoded_genes)
    # columns = ,Tile,X,Y,Barcode,Gene

    nr_recognized_barcodes = 0
    nr_unrecognized_barcodes = 0

    #key = genes to be recognized, value = how many times that gene was found
    gene_dict = {}

    ## key = tile, value = list where number first element = nr recognized, second = nr unrecognized
    # This is used to determine wether some tiles might have strange behaviour
    tile_dict = {}
    for row in df.itertuples():
        tile = row.Tile
        gene = row.Gene
        if tile not in tile_dict:
            tile_dict[tile] = [0,0]
        
        recognized = False if str(gene)=="nan" else True # Pandas converts an empty cell into a 'nan', which is of type float.
        if recognized:
            nr_recognized_barcodes += 1
            tile_dict[tile][0] += 1
            gene_dict[gene] = gene_dict.get(gene, 0)
        else:
            nr_unrecognized_barcodes += 1
            tile_dict[tile][1] += 1


    print(f"Number of recognized barcodes: {nr_recognized_barcodes} \t Number of unrecognized barcodes: {nr_unrecognized_barcodes}. \n Ratio = {round((nr_recognized_barcodes/(nr_unrecognized_barcodes+nr_recognized_barcodes)),3)*100} percent. \n")

    #Add a barcode column to the gene dict, for debugging purposes
    gene_dict = {gene: [gene,count, df.loc[df['Gene']==gene].iloc[0]['Barcode']] for gene, count in gene_dict.items()}
    print("Distribution of recognized barcodes:")
    gene_df = pd.DataFrame.from_dict(list(sorted(gene_dict.values(),key=lambda x: x[1], reverse=True)))
    gene_df.columns=['Gene', 'Counts', 'Barcode']
    gene_df.to_csv("recognized_barcodes.csv")
    fig= plt.figure(figsize=(13,9))

    plt.plot(gene_df['Barcode'], gene_df['Counts'], 'o')
    plt.title("Barcode counts")
    plt.xlabel("Barcode combination")
    plt.ylabel("Number of times recognized")
    plt.savefig("barcode_counts.pdf")
    # print(tabulate(gene_df, headers=["Gene", "Counts", "Barcode"]))

decoded_genes = sys.argv[1]
countRecognizedBarcodeStats(decoded_genes)
countChannelsInBarcodeList(decoded_genes)
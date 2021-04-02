import os 
import pandas as pd
from tabulate import tabulate
from icecream import ic


def debugChannelCalling(path_to_decoded_genes: str):
    df = pd.read_csv(path_to_decoded_genes)

    barcodes = df['']

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
            if gene in gene_dict:
                gene_dict[gene] += 1
            else:
                gene_dict[gene] = 1
        else:
            nr_unrecognized_barcodes += 1
            tile_dict[tile][1] += 1
    print(f"Number of recognized barcodes: {nr_recognized_barcodes} \t Number of unrecognized barcodes: {nr_unrecognized_barcodes}. \n Ratio = {round((nr_recognized_barcodes/(nr_unrecognized_barcodes+nr_recognized_barcodes)),3)*100} percent. \n")

    #Add a barcode column to the gene dict, for debugging purposes
    gene_dict = {gene: [gene,count, df.loc[df['Gene']==gene].iloc[0]['Barcode']] for gene, count in gene_dict.items()}
    print("Distribution of recognized barcodes:")
    gene_df = pd.DataFrame.from_dict(list(sorted(gene_dict.values(),key=lambda x: x[1], reverse=True)))
    gene_df.to_html("test.html")
    print(tabulate(gene_df, headers=["Gene", "Counts", "Barcode"]))

countRecognizedBarcodeStats("/media/tool/moved_from_m2/cartana_test_stitched/results/decoded/concat_decoded_genes.csv")
debugChannelCalling("/media/tool/moved_from_m2/cartana_test_stitched/results/decoded/concat_decoded_genes.csv")
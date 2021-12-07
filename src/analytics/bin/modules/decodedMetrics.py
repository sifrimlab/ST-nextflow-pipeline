import pandas as pd
import os
import matplotlib.pyplot as plt
import random
import numpy as np
import seaborn as sns

def countChannelsInBarcodeList(path_to_decoded_genes: str):
    '''
    This function focuses on all stats that are purely based on how many times a certain channel was called, in what round.
    This can be useful in debugging certain weird decoding behaviour, like finding wether a channel is overexpressed.
    '''
    df = pd.read_csv(path_to_decoded_genes)

    barcodes = list(df['Barcode'])
    # resulting df will have the following columns:
    # 'Channel' 'Round' 'total channel count'
    total_channel_counts= {}
    channel_dict = {} # takes tuples of round/channel as key, and number of times encountered as value 

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
    # Create the rows in the dataframe by representing them as dataframes
    for k,count in channel_dict.items():
        temp_dict = {}
        round_nr, channel_nr = k
        row_values = [round_nr, channel_nr, count]
        temp_dict = {col_names[i]: row_values[i] for i in range(0,len(col_names)) }
        rows_list.append(temp_dict)
    count_df = pd.DataFrame(rows_list)
    wide_df = count_df.pivot_table(index=["channel_nr"], columns='round_nr', values='count', margins=True, aggfunc='sum')
    wide_df.to_html("channels_called.html", index=False)

    
def evaluateRandomCalling(path_to_decoded_genes: str, path_to_codebook: str, num_rounds: int, num_channels: int, ratio_recognized_barcodes: int = 0, simulate=False):
        codebook_df = pd.read_csv(path_to_codebook)
        decoded_df = pd.read_csv(path_to_decoded_genes)
        # Attribute dicts is going to collect all columns of the only row the analytics df will have, key=column name, value = column value
        attribute_dict={}
        n_genes_to_find=len(codebook_df)
        attribute_dict['# genes in codebook'] = n_genes_to_find
        n_spots= len(decoded_df)
        attribute_dict['# spots detected']= n_spots


        # Create the counted column
        decoded_df['Counted'] = decoded_df.groupby('Barcode')['Gene'].transform('size') # count every barcode-gene combination and make a new column out of it
        unique_df = decoded_df[['Barcode', 'Counted']].drop_duplicates()
        unique_df = unique_df.sort_values(by=['Counted'], ascending=False)
        non_recognized_barcodes = [barcode for barcode in list(unique_df['Barcode']) if barcode not in list(codebook_df['Barcode'])]
        non_recognized_df= unique_df[unique_df.Barcode.isin(non_recognized_barcodes)]
        
        unique_df.to_html("unique_barcodes_called_counted.html", index=False)

        color_list = ['green' if barcode in list(codebook_df['Barcode']) else 'red' for barcode in decoded_df['Barcode']] 
        fig= plt.figure(figsize=(13,9))
        plt.scatter(decoded_df['Barcode'], decoded_df['Counted'], c = color_list)
        plt.title("Barcodes counted")
        plt.xlabel("Barcode combination")
        plt.ylabel("Number of times recognized")
        plt.savefig("barcodes_counted.png")

        # Evaluate randomness
        possible_barcode_combinations = int(num_channels) ** int(num_rounds)
        n_unique_barcodes_called = len(unique_df)
        n_random_calls_expected_per_barcode = n_spots/possible_barcode_combinations
        ratio_recognized_barcodes_random_calling_would_create = round(((n_random_calls_expected_per_barcode * n_genes_to_find) / n_spots), 3) *100

        
        # Add to the row entry
        attribute_dict['# possible combination'] = possible_barcode_combinations
        attribute_dict['# unique barcodes called'] = n_unique_barcodes_called
        attribute_dict['# calls per barcode combination expected if random calling'] = n_random_calls_expected_per_barcode
        attribute_dict['Random recognized ratio'] = ratio_recognized_barcodes_random_calling_would_create
        rows_list=[]
        rows_list.append(attribute_dict)
        analytics_df = pd.DataFrame(rows_list)
        analytics_df.to_html("decoded_stat.html", index=False)

    
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
    # general_attribute_dict: key=column name, value = column value
    general_attribute_dict = {}
    for row in df.itertuples():
        tile = row.Tile
        gene =str(row.Gene)
        if tile not in tile_dict:
            # T0,0] = tuple representing nr_recognized_barcodes,nr_unrecognized_barcodes
            tile_dict[tile] = [0,0]
        
        recognized = False if str(gene)=="nan" else True # Pandas converts an empty cell into a 'nan', which is of type float.
        if recognized:
            nr_recognized_barcodes += 1
            tile_dict[tile][0] += 1
            gene_dict[gene] = gene_dict.get(gene, 0)+1 # This creates the key if it isn't there already
        else:
            nr_unrecognized_barcodes += 1
            tile_dict[tile][1] += 1

    general_attribute_dict['# recognized barcodes']= nr_recognized_barcodes
    general_attribute_dict['# unrecognized barcodes']= nr_unrecognized_barcodes
    general_attribute_dict['Total # spots']= len(df)
    general_attribute_dict['Ratio']= round((nr_recognized_barcodes/(len(df))),3)*100
    general_row_list = []
    general_row_list.append(general_attribute_dict)
    general_df = pd.DataFrame(general_row_list)
    general_df.to_html("general_stats.html", index=False)

    # Now we parse the tile dicts
    tile_row_list= []
    for tile_nr, count_list in tile_dict.items():
        # tile_attribute_dict: key=column name, value = column value
        tile_attribute_dict = {}
        tile_attribute_dict['Tile']= tile_nr
        nr_recognized_barcodes, nr_unrecognized_barcodes = count_list
        tile_attribute_dict['# recognized barcodes']= nr_recognized_barcodes
        tile_attribute_dict['# unrecognized barcodes']= nr_unrecognized_barcodes
        tile_attribute_dict['Ratio']=round((nr_recognized_barcodes/(nr_unrecognized_barcodes + nr_recognized_barcodes)),3)*100 
        tile_row_list.append(tile_attribute_dict)

    tile_df = pd.DataFrame(tile_row_list)
    tile_df = tile_df.sort_values(by=['Tile'])
    tile_df.to_html("tile_stats.html", index=False)

    # Create a Barpot plotting recognized an unrecognized genes per tile, for quality control purposes

    labels = tile_df['Tile']
    recognized_column = tile_df['# recognized barcodes']
    unrecognized_column = tile_df['# unrecognized barcodes']

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, recognized_column, width, label='recognized')
    rects2 = ax.bar(x + width/2, unrecognized_column, width, label='unrecognized')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('# barcodes')
    ax.set_xlabel('Tile number')
    ax.set_title('# number of barcodes recognized by tile')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)
    fig.tight_layout()
    plt.savefig("recognized_genes_per_tile.png")


    

    # parse the dict such that the value becomes gene name, count, and respective barcode. this makes it easier to convert to a df
    gene_dict = {gene: [gene,count, df.loc[df['Gene']==gene].iloc[0]['Barcode']] for gene, count in gene_dict.items()}
    gene_df = pd.DataFrame.from_dict(list(sorted(gene_dict.values(),key=lambda x: x[1], reverse=True)))
    print(gene_df)
    gene_df.columns=['Gene', 'Counts', 'Barcode']
    gene_df.to_html("recognized_barcodes_per_gene.html", index=False)

    fig= plt.figure(figsize=(13,9))
    plt.plot(gene_df['Gene'], gene_df['Counts'], 'o')
    plt.title("Recognized genes counted")
    plt.xlabel("Gene name")
    plt.ylabel("Number of times recognized")
    plt.savefig("recognized_genes_counts.png")

def getGeneralMerfishStats(decoded_genes: str, codebook: str):
    sns.set_theme()
    decoded_genes_df = pd.read_csv(decoded_genes)
    codebook_df = pd.read_csv(codebook)

    # calculate average area and distance
    areas = list(decoded_genes_df['area'])
    distances =  list(decoded_genes_df['Distance'])
    avg_area = np.mean(areas)
    avg_distance = np.mean([float(distance) for distance in distances])

    n_genes = len(decoded_genes_df)

    # Making distribution plots
    fig, axs = plt.subplots(1,2)
    axs[0].set_title("Area distribution", fontweight="bold")
    sns.histplot(areas, bins=np.arange(min(areas), max(areas)+2) -0.5, kde=True, ax=axs[0], color="blue")
    axs[0].set_xticks(range(min(areas),max(areas) +1))
    for rect in axs[0].patches:
        height = rect.get_height()
        axs[0].annotate(f'{int(height)}', xy=(rect.get_x()+rect.get_width()/2, height),xytext=(0, 5), textcoords='offset points', ha='center', va='bottom')

    axs[1].set_title("Distance distribution",fontweight="bold" )
    sns.histplot(distances, kde=True, ax=axs[1], color="red")
    for rect in axs[1].patches:
        height = rect.get_height()
        axs[1].annotate(f'{int(height)}', xy=(rect.get_x()+rect.get_width()/2, height),xytext=(0, 5), textcoords='offset points', ha='center', va='bottom')


    # Caclulate gene counts
    decoded_genes_df = decoded_genes_df.dropna(subset=["Gene"])
    decoded_genes_df['Counted'] = decoded_genes_df.groupby('Gene')['Gene'].transform('size') # count every barcode-gene combination and make a new column out of it
    unique_df = decoded_genes_df[['Gene', 'Counted']].drop_duplicates()

    # Count how many genes have Counted == 1
    n_1_genes =(len(unique_df.loc[unique_df['Counted'] == 1]))

    unique_df = unique_df.sort_values(by=['Counted'], ascending=False)
    unique_df_top10 = unique_df.head(10)


    unique_df = unique_df.sort_values(by=['Counted'], ascending=True)
    unique_df_bot10 = unique_df.head(10)


    # create general stats table
    row_list = []
    attribute_dict = {}
    attribute_dict['# decoded spots'] = n_genes
    attribute_dict['Average area'] = avg_area
    attribute_dict['Average distance'] = avg_distance
    attribute_dict['# one-shot genes'] = n_1_genes

    row_list.append(attribute_dict)

    general_stats_df = pd.DataFrame(row_list)
    general_stats_df.to_html("general_stats.html", index=False)

    unique_df_top10.to_html("top10_genes.html", index=False)
    unique_df_bot10.to_html("bot10_genes.html", index=False)


    plt.savefig("distributions.png")




if __name__ == '__main__':
    decoded_genes = "./concat_decoded_genes.csv"
    codebook = "/home/david/Documents/communISS/data/merfish/codebook.csv"
    getGeneralMerfishStats(decoded_genes, codebook)
        # countChannelsInBarcodeList(decoded_genes)
        # evaluateRandomCalling(decoded_genes, codebook, 4,4)
        # countRecognizedBarcodeStats(decoded_genes)

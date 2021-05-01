import pandas as pd
import os
import matplotlib.pyplot as plt
import random
import numpy as np

def countGeneralAssignedStats(assigned_genes_csv: str):
    df = pd.read_csv(assigned_genes_csv)
    df['Cell_Count'] = df.groupby('Cell_Label')['Cell_Label'].transform('count')

    # General stats
    nr_not_assigned  = df.loc[ df['Cell_Label']=="0"]['Cell_Count'][0]
    nr_assigned = len(df) - nr_not_assigned
    ratio_assigned = round(nr_assigned/len(df), 3)*100


    fig, axs = plt.subplots(1,1)
    axs.hist(list(df['area']))
    axs.set_title("Histogram of the area of the detected spots")
    axs.set_xlabel("Area in # pixels")
    axs.set_ylabel("Times encountered")
    axs.set_yticks([])
    for rect in axs.patches:
        height = rect.get_height()
        axs.annotate(f'{int(height)}', xy=(rect.get_x()+rect.get_width()/2, height), 
                    xytext=(0, 5), textcoords='offset points', ha='center', va='bottom')
    fig.tight_layout()
    plt.show()
    print(df.columns)

    # grouped_by_cell_gene_counts = df.groupby(['Cell_Label'])['Cell_Count'].size()
    # pd.DataFrame(grouped_by_cell_gene_counts).to_html("per_cell_gene_counts.html")


"""
ideas:
- area distributio
- # assigned vs non-assigned
- QC metric for segmentation (op basis van properties): average/min/max intensity van segmented cells -> wijst aan of dapi juist is
"""
if __name__ == '__main__':
        assigned_genes = "/media/david/Puzzles/starfish_test_data/MERFISH/seperate_stacks_cropped/results_tiled_whitetophat/assigned/concat_assigned_genes.csv" 
        countGeneralAssignedStats(assigned_genes)

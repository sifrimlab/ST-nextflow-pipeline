import pandas as pd
import os
import matplotlib.pyplot as plt
import random
import numpy as np

def countGeneralAssignedStats(assigned_genes_csv: str, merfish = False):
    df = pd.read_csv(assigned_genes_csv)
    df['n_genes_in_cell'] = df.groupby('Cell_Label')['Cell_Label'].transform('count')
    df['n_times_gene_counted'] = df.groupby('Gene')['Gene'].transform('count')
    # columns = 'Spot_label', 'area', 'Y', 'X', 'Barcode', 'Distance', 'Gene','Gene_Label', 'Tile', 'Cell_Label
    df_only_assigned = df[df['Cell_Label']!="0"] # For extracting most assigned cells

    # General stats
    try:
        nr_not_assigned  = len(df.loc[ df['Cell_Label']=="0"])
    # It might be with voronoi asisgnment that there is actually not a single unassigned gene, i nthis case this just needs to be zero
    except KeyError:
        nr_not_assigned = 0
    nr_assigned = len(df) - nr_not_assigned
    ratio_assigned = round(nr_assigned/len(df), 3)*100

    general_attributes = {}
    general_attributes["# Assigned to cells"] = nr_assigned
    general_attributes["# Unassigned to cells"] = nr_not_assigned
    general_attributes["Ratio"] = ratio_assigned
    rows_list =  []
    rows_list.append(general_attributes)
    general_table = pd.DataFrame(rows_list)
    general_table.to_html("general_assignment_information.html", index=False)

    # Area of spots
    if merfish:
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
        plt.savefig("area_of_pixels_counted.png")

        # number of spots per cell
        grouped_by_cell_gene_counts = df.groupby(['Cell_Label'])['n_genes_in_cell'].size()
        pd.DataFrame(grouped_by_cell_gene_counts).to_html("per_cell_gene_counts.html", index=False)
    # Cells with the highest expression
    df_sorted_cells = df_only_assigned.sort_values(by=['n_genes_in_cell'], ascending=False,ignore_index=True)
    df_sorted_cells = df_sorted_cells.drop_duplicates(subset=['Cell_Label'])
    df_top_10 = df_sorted_cells.head(10)
    df_top_10 = df_top_10[['Tile', 'Cell_Label','n_genes_in_cell']]
    df_top_10.to_html("top10_assigned_cells.html", index=False)



    # highest expressed genes in cells
    df_sorted_genes = df_only_assigned.sort_values(by=['n_times_gene_counted'], ascending=False, ignore_index=True)
    df_sorted_genes = df_sorted_genes.drop_duplicates(subset=['Gene'])
    df_top_10 = df_sorted_genes.head(10)
    df_top_10 = df_top_10[['Tile', 'Gene','n_times_gene_counted']]
    df_top_10.to_html("top10_assigned_genes.html", index=False)


"""
ideas:
- QC metric for segmentation (op basis van properties): average/min/max intensity van segmented cells -> wijst aan of dapi juist is
 - highest expressed gene
"""
if __name__ == '__main__':
        # assigned_genes = "/media/david/Puzzles/starfish_test_data/MERFISH/seperate_stacks_cropped/results_tiled_whitetophat/assigned/concat_assigned_genes.csv" 
        assigned_genes = "/media/david/Puzzles/gabriele_data/1442_OB/assigned/concat_assigned_genes.csv"
        countGeneralAssignedStats(assigned_genes)

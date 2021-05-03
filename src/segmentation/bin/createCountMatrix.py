import os 
import sys
import pandas as pd
import numpy as np


def createCountMatrix(assigned_genes:str):
    original_df = pd.read_csv(assigned_genes)
    original_df = original_df[original_df.Cell_Label != 0]
    df1 = pd.crosstab(original_df.Gene,original_df.Cell_Label,original_df.Cell_Label,aggfunc='count').fillna(0)
    df2 = original_df.groupby('Gene')['Cell_Label'].value_counts().unstack('Cell_Label', fill_value=0).reset_index()
    return df1




assigned_genes = sys.argv[1]
# prefix = os.path.splitext(assigned_genes)[0]
count_matrix = createCountMatrix(assigned_genes)
count_matrix.to_csv("count_matrix.csv")


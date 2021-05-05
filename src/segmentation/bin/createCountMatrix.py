import os 
import sys
import pandas as pd
from modules.geneExpressionMatrices import createCountMatrix






assigned_genes = sys.argv[1]
# prefix = os.path.splitext(assigned_genes)[0]
count_matrix = createCountMatrix(assigned_genes)
count_matrix.to_csv("count_matrix.csv")


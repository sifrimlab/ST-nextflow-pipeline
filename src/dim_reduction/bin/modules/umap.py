import numpy as np

import scanpy as sc
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
import seaborn as sb
# from gprofiler import GProfiler

# import rpy2.rinterface_lib.callbacks
import logging

# from rpy2.robjects import pandas2ri
import anndata2ri


# normalize
# clusters met pca

# def qualityControl(count_matrix):
# # Quality control - calculate QC covariates
#     adata.obs['n_counts'] = adata.X.sum(1)
#     adata.obs['log_counts'] = np.log(adata.obs['n_counts'])
#     adata.obs['n_genes'] = (adata.X > 0).sum(1)

#     mt_gene_mask = [gene.startswith('mt-') for gene in adata.var_names]
#     adata.obs['mt_frac'] = adata.X[:, mt_gene_mask].sum(1)/adata.obs['n_counts']

if __name__ == '__main__':
    count_matrix = "RawRNAcounts_2k_features.csv"
    data = scanpy.read(count_matrix)
    print(data)




import numpy as np

import scanpy as sc
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
# import seaborn as sb
# from gprofiler import GProfiler

# import rpy2.rinterface_lib.callbacks
# import logging

# from rpy2.robjects import pandas2ri
# import anndata2ri


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
    adata = sc.read(count_matrix, cache=True)
    # adata.obs_names = genes x adata.var_names = cells
    # adata.obs['n_counts'] = adata.X.sum(0)
    # adata.obs['log_counts'] = np.log(adata.obs['n_counts'])
    # adata.obs['n_genes'] = (adata.X > 0).sum(0)

    # good for in the future, not right now
    # mt_gene_mask = [gene.startswith('mt-') for gene in adata.obs_names]

    # normalization and clustering
    # adata_pp = adata.copy()
    # sc.pp.normalize_per_cell(adata_pp, counts_per_cell_after=1e6)
    # sc.pp.log1p(adata_pp)
    # sc.pp.pca(adata_pp, n_comps=15)
    # sc.pp.neighbors(adata_pp)
    # sc.tl.louvain(adata_pp, key_added='groups', resolution=0.5)

    
    # Calculate the visualizations
    # sc.pp.highly_variable_genes(adata, flavor='cell_ranger', n_top_genes=2000)
    # print('\n','Number of highly variable genes: {:d}'.format(np.sum(adata.var['highly_variable'])))

    sc.pp.pca(adata, n_comps=50,  svd_solver='arpack')
    sc.pp.neighbors(adata)
    sc.tl.umap(adata)
    sc.tl.diffmap(adata)
    print(sc.tl.draw_graph(adata))

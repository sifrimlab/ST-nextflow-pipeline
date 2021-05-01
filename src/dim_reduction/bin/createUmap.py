import os
import sys
import matplotlib.pyplot as plt
from modules.countMatrixUmap import createAndPlotUmap


count_matrix = sys.argv[1]
umap = createAndPlotUmap(count_matrix)
umap.savefig("count_matrix_umap.svg")

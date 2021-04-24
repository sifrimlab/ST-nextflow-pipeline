import os 
import matplotlib.pyplot as plt
import sys
from modules.decodingPotential import plotDecodingPotential

decoded_genes = sys.argv[1]
prefix = os.path.splitext(decoded_genes)[0]
codebook = sys.argv[2]

plt = plotDecodingPotential(decoded_genes, codebook)
plt.title(f"{prefix} decoding potential per round")
plt.savefig(f"{prefix}_decoding_potential_plot.svg")

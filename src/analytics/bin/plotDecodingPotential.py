import os 
import matplotlib.pyplot as plt
import sys
from modules.decodingPotential import plotDecodingPotential.py

decoded_genes = sys.argv[1]
codebook = sys.argv[2]

plt = plotDecodingPotential(decoded_genes, codebook)
plt.savefig("decoding_potential_plot.svg")

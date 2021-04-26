import sys
from modules.imageViewing import plotDecodedGenesOnTile 
import matplotlib.pyplot as plt
import os

tile_image = sys.argv[1]
decoded_genes = sys.argv[2]
radius =  int(sys.argv[3])
prefix = os.path.splitext(decoded_genes)[0]
plt = plotDecodedGenesOnTile(tile_image, decoded_genes,radius)
    # fig.savefig('myimage.svg', format='svg', dpi=1200)
plt.savefig(f"{prefix}_plotted.svg", format='svg', dpi=1200)

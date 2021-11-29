import sys
import os
from modules.plotGenes import plotGeneExpression

image = sys.argv[1]
decoded_genes = sys.argv[2]
barcode = sys.argv[3]
image_prefix = os.path.splitext(image)[0]
barcode = os.path.splitext(barcode)[0]
prefix = f"{image_prefix}_{barcode}_expression_plotted"

plot=plotGeneExpression(image, decoded_genes, barcode)
plot.savefig(f"{prefix}.png")




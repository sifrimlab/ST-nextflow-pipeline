import matplotlib.pyplot as plt
from modules.plotSegmentation import plotAssignedGenes
import numpy as np
import pandas as pd
from skimage import io, color
import sys
import os


assigned_genes = sys.argv[1]
labeled_image = sys.argv[2]
prefix = os.path.splitext(labeled_image)[0]

plt=plotAssignedGenes(assigned_genes, labeled_image)
plt.savefig(f"{prefix}_plotted.svg", format="svg", dpi=12000)

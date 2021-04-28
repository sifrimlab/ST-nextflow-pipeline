import matplotlib.pyplot as plt
from modules.plotSegmentation import plotAssignedGenes
import numpy as np
import pandas as pd
from skimage import io, color
import sys
import os


assigned_genes = sys.argv[1]
labeled_image = sys.argv[2]
prefix = os.path.splitext(assigned_genes)[0]
plotAssignedGenes(assigned_genes, labeled_image, prefix)

import sys
from modules.imageViewing import plotSpotsOnTile
import matplotlib.pyplot as plt
import os

tile_image = sys.argv[1]
detected_spots = sys.argv[2]
radius =  int(sys.argv[3])
prefix = os.path.splitext(detected_spots)[0]
plt = plotSpotsOnTile(tile_image, detected_spots,radius)
plt.savefig(f"{prefix}_plotted.tif")

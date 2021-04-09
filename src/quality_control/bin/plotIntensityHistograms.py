from modules.intensities import plotHistograms, getHistogram
import sys
import os

image = sys.argv[1]
prefix = os.path.splitext(image)[0]
plt = plotHistograms({prefix:getHistogram(image)})
plt.savefig(f"{prefix}_intensity_histogram.svg", format="svg")

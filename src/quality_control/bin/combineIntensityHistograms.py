from modules.intensities import getHistogram, plotCombinedHistograms
import sys
import os

prefix = sys.argv[1]
images = [sys.argv[i] for i in range(2, len(sys.argv))]
hist_dict = {os.path.splitext(image)[0]: getHistogram(image) for image in images}
plt = plotCombinedHistograms(hist_dict, f"{prefix} intensity histograms")
plt.savefig(f"{prefix}_intensity_histogram.svg", format="svg")

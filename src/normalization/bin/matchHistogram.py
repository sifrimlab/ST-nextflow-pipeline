import os
import sys
from skimage import io
from modules.histogramNormalizing import matchHistograms

reference = sys.argv[1]
target = sys.argv[2]
prefix = os.path.splitext(reference)[0]
matched = matchHistograms(reference, target)
io.imwrite(f"{prefix}_matched.tif", matched)

import os 
import pandas as pd
import matplotlib.pyplot as plt
import sys
import random
import numpy as np
from modules.decodedMetrics import countRecognizedBarcodeStats, countChannelsInBarcodeList, evaluateRandomCalling, getGeneralMerfishStats

decoded_genes = sys.argv[1]
codebook = sys.argv[2]
technique = sys.argv[3]
if technique == "iss":
    n_rounds = sys.argv[4]
    n_channels = sys.argv[5]


if technique == "iss":
    countRecognizedBarcodeStats(decoded_genes)
    countChannelsInBarcodeList(decoded_genes)
    evaluateRandomCalling(decoded_genes, codebook, n_rounds, n_channels)
if technique == "merfish":
    getGeneralMerfishStats(decoded_genes, codebook)




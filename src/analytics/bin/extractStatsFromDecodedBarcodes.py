import os 
import pandas as pd
import matplotlib.pyplot as plt
import sys
import random
import numpy as np
from modules.decodedMetrics import countRecognizedBarcodeStats, countChannelsInBarcodeList, evaluateRandomCalling 

decoded_genes = sys.argv[1]
codebook = sys.argv[2]
n_rounds = sys.argv[3]
n_channels = sys.argv[4]


countRecognizedBarcodeStats(decoded_genes)
countChannelsInBarcodeList(decoded_genes)
evaluateRandomCalling(decoded_genes, codebook, n_rounds, n_channels)




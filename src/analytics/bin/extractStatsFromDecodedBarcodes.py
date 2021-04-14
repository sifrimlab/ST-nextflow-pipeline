import os 
import pandas as pd
from tabulate import tabulate
from icecream import ic
import matplotlib.pyplot as plt
import sys
import random
import numpy as np
from modules.decodedMetrics.py import countRecognizedBarcodeStats, countChannelsInBarcodeList

decoded_genes = sys.argv[1]
codebook = sys.argv[2]
n_rounds = sys.argv[3]
n_channels = sys.argv[4]

countRecognizedBarcodeStats(decoded_genes)
countChannelsInBarcodeList(decoded_genes)
evaluateRandomCalling(decoded_genes, codebook, n_rounds, n_channels)

import os 
import pandas as pd
import matplotlib.pyplot as plt
import sys
import random
import numpy as np
from modules.decodedMetrics import countRecognizedBarcodeStats

decoded_genes = sys.argv[1]

countRecognizedBarcodeStats(decoded_genes)

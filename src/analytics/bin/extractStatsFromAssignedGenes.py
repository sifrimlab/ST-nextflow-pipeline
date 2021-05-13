import os 
import sys
import random
import numpy as np
from modules.assignedMetrics import countGeneralAssignedStats

assigned_genes = sys.argv[1]

countGeneralAssignedStats(assigned_genes)

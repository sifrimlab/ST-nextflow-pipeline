import sys
from modules.decodedMetrics import getGeneralMerfishStats

decoded_genes = sys.argv[1]
codebook = sys.argv[2]

getGeneralMerfishStats(decoded_genes, codebook)

import sys
import pandas as pd
from modules.intensityParsing import getMaxIntensityPerRound
# codebook = pd.read_csv("/media/tool/starfish_test_data/ExampleInSituSequencing/codebook.csv")

# df_total = pd.read_csv("/media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/results2/intensities/concat_intensities.csv")


# Argparsing
path_to_intensity_csv = sys.argv[1]
getMaxIntensityPerRound(path_to_intensity_csv)








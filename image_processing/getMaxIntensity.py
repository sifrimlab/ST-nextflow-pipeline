import pandas as pd 
import csv
import sys
# codebook = pd.read_csv("/media/tool/starfish_test_data/ExampleInSituSequencing/codebook.csv")

# df_total = pd.read_csv("fake_intensities.csv")




def getMaxIntensityPerRound(path_to_intensity_csv: str):
    df_total = pd.read_csv(path_to_intensity_csv)
    # Calculate max tile nr.
    n_tiles = df_total['Tile'].max()
    # First I split the df up into a dataframe for each tile, cause the tiles don't need to interact with each other.
    unique_tiles = df_total.Tile.unique()
    df_dict = {tile : pd.DataFrame for tile in unique_tiles}
    for key in df_dict.keys():
        df_dict[key] = df_total[:][df_total.Tile == key]
    # End result: each tile is now in a different df, stored inside the df_dict, with tile nr as key
    for i in range(1, n_tiles+1):
        df = df_dict[i].drop(columns='Tile') # Tile column doesn't matter anymore
        df_filtered = df.sort_values('Intensity', ascending=False).drop_duplicates(['Round','Y','X'])
        # Different implementation; gets ALL maxima, but slightly slower: df_filtered = df[df.groupby(['Round','Y','X'])['Intensity'].transform(max)== df['Intensity']]
        # Print out into different csv's to fascilitate parallelizing in nextflow
        df_filtered.to_csv(f"tile{i}_max_intensities.csv")


# Argparsing
path_to_intensity_csv = sys.argv[1]
getMaxIntensityPerRound(path_to_intensity_csv)

# 







import pandas as pd 
import csv

n_tiles = 4
n_channels = 4 
n_rounds=4
codebook = pd.read_csv("/media/tool/starfish_test_data/ExampleInSituSequencing/codebook.csv")

df_total = pd.read_csv("/home/nacho/Documents/Code/communISS/results/intensities/concat_intensities.csv")
# First I split the df up into a dataframe for each tile, cause the tiles don't need to interact with each other.
unique_tiles = df_total.Tile.unique()
df_dict = {tile : pd.DataFrame for tile in unique_tiles}

for key in df_dict.keys():
    df_dict[key] = df_total[:][df_total.Tile == key]

# End result: each tile is not in a different df, stored inside the df_dict.

# Let's just start with tile 2, now we can 
for i in range(1, n_tiles+1):
    df = df_dict[i].drop(columns='Tile') # Tile column doesn't matter anymore
    df.groupby(['Round','Y','X']).max().to_csv(f"tile{i}_max.csv")

# max_int = 0
# winning_channel = 0
# for row in df2.itertuples():
#     if row.Round == 1 and row.Y == 47 and row.X == 576:
#         if row.Intensity > max_int:
#             max_int = row.Intensity
#             winning_channel = row.Channel
# print(max_int, winning_channel)



# This is a cool pandas excerpt to count how many unique combinations exist in a dataframe.
#df2.groupby(['Y','X', 'Round']).size().reset_index().rename(columns={0:'count'})

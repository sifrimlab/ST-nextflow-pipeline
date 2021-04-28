import sys
from icecream import ic
import pandas as pd

def getMaxIntensityPerRound(path_to_intensity_csv: str):
    # function to calculate Imax/(Ia + Ig + It + Ic)
    def calcQC(intensity_list):
        mx = max(intensity_list)
        sm = sum(intensity_list)
        try:
            return float(mx/sm)
        except ZeroDivisionError:
            return 0

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
        try:
            df = df_dict[i].drop(columns='Tile') # Tile column doesn't matter anymore
            df['Intensity_ratio']=df.groupby(['Round','Y','X'])['Intensity'].transform(calcQC)
            df_filtered = df.sort_values('Intensity', ascending=False).drop_duplicates(['Round','Y','X'])
            # Print out into different csv's to fascilitate parallelizing in nextflow
            df_filtered.to_csv(f"tile{i}_max_intensities.csv", index=False)
        except KeyError:
            pass





if __name__=='__main__':
    intensities = "/media/tool/gabriele_data/1442_OB/maxIP-seperate-channels/results_correct_codebook_white_disk3_minsigma2_maxsigma20_second_attempts/intensities/concat_intensities.csv"
    getMaxIntensityPerRound(intensities)

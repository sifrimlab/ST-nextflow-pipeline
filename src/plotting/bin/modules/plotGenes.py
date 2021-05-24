import pandas as pd
import matplotlib.pyplot as plt
from skimage import io
import numpy as np
from sklearn.metrics import r2_score

def plotGeneExpression(image_path: str, decoded_genes: str, barcode: int):
    img  = io.imread(image_path)
    decoded_genes= pd.read_csv(decoded_genes)
    filtered_spots = decoded_genes[decoded_genes['Barcode'] == barcode]
    fig, ax = plt.subplots(1,1)
    ax.imshow(img, cmap='gray')
    for row in filtered_spots.itertuples():
        circ = plt.Circle((row.X, row.Y), radius=2, color="w")
        ax.add_patch(circ)
    return plt

def plotGeneCountDistribution(decoded_genes, top_genes=10):
    decoded_df = pd.read_csv(decoded_genes)
    decoded_df = decoded_df.dropna(subset=["Gene"])
    decoded_df['Counted'] = decoded_df.groupby('letters')['Gene'].transform('size') # count every barcode-gene combination and make a new column out of it
    unique_df = decoded_df[['Gene', 'letters', 'Counted']].drop_duplicates()
    unique_df = unique_df.sort_values(by=['Counted'], ascending=False)
    unique_df_top10 = unique_df.head(top_genes)

    fig, ax = plt.subplots(1,1)
    ax.bar(unique_df_top10['Gene'], unique_df_top10['Counted'], color="cornflowerblue")
    for rect in ax.patches:
        height = rect.get_height()
        ax.annotate(f'{int(height)}', xy=(rect.get_x()+rect.get_width()/2, height),
                    xytext=(0, 10), textcoords='offset points', ha='center', va='bottom')
    ax.plot(unique_df_top10['Gene'], unique_df_top10['Counted'], "o-k")
    ax.set_xlabel("Top 10 expressed genes")
    ax.set_ylabel("Times decoded")
    plt.show()
    # plt.savefig("OB_gene_expression_top10.svg", format="svg")
def plotGeneCountR2(decoded_genes1, decoded_genes2):
    decoded_df1 = pd.read_csv(decoded_genes1)
    decoded_df2 = pd.read_csv(decoded_genes2)
    decoded_df1 = decoded_df1.dropna(subset=["Gene"])
    decoded_df2 = decoded_df2.dropna(subset=["Gene"])

    decoded_df1['Counted_1'] = decoded_df1.groupby('Barcode')['Gene'].transform('size') # count every barcode-gene combination and make a new column out of it
    decoded_df2['Counted_2'] = decoded_df2.groupby('letters')['Gene'].transform('size') # count every barcode-gene combination and make a new column out of it

    unique_df1 = decoded_df1[['Gene', 'Barcode', 'Counted_1']].drop_duplicates()
    unique_df1 = unique_df1.sort_values(by=['Gene'], ascending=False)
    unique_df2 = decoded_df2[['Gene', 'letters', 'Counted_2']].drop_duplicates()
    unique_df2 = unique_df2.sort_values(by=['Gene'], ascending=False)

    combined_df = unique_df1.merge(unique_df2,on="Gene", how="outer")
    combined_df = combined_df.fillna(0)
    convert_dict = {'Counted_1': int,
                    'Counted_2': int }
    combined_df= combined_df.astype(convert_dict)
    
    # Calculate R²
    combined_only_counted = combined_df[["Counted_1", "Counted_2"]]
    rsquared_df =np.square( combined_only_counted.corr(method='pearson'))
    # Extract value from df, this is not very elegant
    rsquared =round(list(rsquared_df["Counted_1"])[-1], 4)
    # fit a linear line through it
    x = combined_only_counted["Counted_1"]
    y = combined_only_counted["Counted_2"]
    linear_model=np.polyfit(x,y,1)
    linear_model_fn=np.poly1d(linear_model)
    x_range = np.arange(min(x), max(x))



    _, ax = plt.subplots(1,1)
    ax.scatter(combined_only_counted["Counted_1"], combined_only_counted["Counted_2"], color="maroon")
    ax.set_xlabel("Dissertation's gene counts")
    ax.set_ylabel("Partel et al. gene counts")
    ax.set_title(f"R² as calculated by squaring Pearson's correlation: {rsquared}")

    # plot linear fit
    ax.plot(x_range,linear_model_fn(x_range),color="black", label="Linear function fitted")
    ax.legend(loc="upper left")
    plt.savefig("/media/Puzzles/results_figures/gene_expression/gab_vs_me_r2_plot.png", format="png")





if __name__ == '__main__':
    # image = "/media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/results2/tiled_DO/REF_padded_tiled_3.tif"
    # decoded_genes = "/media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/results2/decoded/decoded_tiled_3.csv"
    # gene_name = "5534"
    # plotGeneExpression(image, decoded_genes, gene_name)

    decoded_genes = "/media/Puzzles/gabriele_data/1442_OB/results_correct_codebook_whiteDisk3_minSigma2_maxSigma20_noNorm_stardistSegmentation/decoded/concat_decoded_genes.csv"
    decoded_genes2 = "/media/Puzzles/gabriele_data/original_data/results/1442_OB/barcodes_corrected.csv"
    plotGeneCountR2(decoded_genes, decoded_genes2)

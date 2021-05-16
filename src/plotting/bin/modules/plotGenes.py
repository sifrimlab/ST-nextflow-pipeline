import pandas as pd
import matplotlib.pyplot as plt
from skimage import io


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





if __name__ == '__main__':
    # image = "/media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/results2/tiled_DO/REF_padded_tiled_3.tif"
    # decoded_genes = "/media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/results2/decoded/decoded_tiled_3.csv"
    # gene_name = "5534"
    # plotGeneExpression(image, decoded_genes, gene_name)

    decoded_genes = "/media/Puzzles/gabriele_data/1442_OB/results_correct_codebook_whiteDisk3_minSigma2_maxSigma20_noNorm_stardistSegmentation/decoded/concat_decoded_genes.csv"
    decoded_genes2 = "/media/Puzzles/gabriele_data/original_data/results/1442_OB/barcodes_corrected.csv"
    plotGeneCountDistribution(decoded_genes2)

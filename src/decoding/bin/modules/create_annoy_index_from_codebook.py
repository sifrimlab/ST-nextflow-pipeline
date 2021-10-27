from annoy import AnnoyIndex
from pixelBasedDecoding import createBarcodeVector
import numpy as np
import pandas as pd


def createAnnoyIndex(codebook_path: str, bit_len:int, n_trees:int):

    def parseBarcodes(codebook: str, bit_len: int):
        df = pd.read_csv(codebook)
        df['Barcode'] = [f"{barcode:0{bit_len}}" for barcode in list(df['Barcode'])]
        df['Index'] = list(range(1,len(df)+1)) 
        df['Vectors'] = [createBarcodeVector(barcode) for barcode in df['Barcode']]
        list_of_codebook_vectors = np.array(df['Vectors'])
        return list_of_codebook_vectors
        # codebook =
    list_of_codebook_vectors = parseBarcodes(codebook_path, 16)
    n_vectors = len(list_of_codebook_vectors)

    t = AnnoyIndex(bit_len, 'euclidean')
    for i in range(0,n_vectors):
        v = list_of_codebook_vectors[i]
        t.add_item(i, v)
    t.build(n_trees)
    t.save("codebook_index.ann")





if __name__ == "__main__":
    codebook_path = "/home/nacho/Documents/communISS/data/merfish/codebook.csv"
    createAnnoyIndex(codebook_path, bit_len=16, n_trees=10)

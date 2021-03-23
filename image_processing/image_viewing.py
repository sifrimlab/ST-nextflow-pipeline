reference = "/media/tool/starfish_test_data/ExampleInSituSequencing/DO/REF.TIF"
blobs = "/home/nacho/Documents/Code/communISS/results/blobs/concat_blobs.csv"


import pandas as pd
import cv2
import numpy as np
df = pd.read_csv(blobs)
print(df.columns)
df1=df[df['Tile']==1]


image = cv2.imread(reference)
empty_image = np.zeros(image.shape)
for row in df1.itertuples():
    empty_image[row.X, row.Y]=255
cv2.imshow("empty", empty_image)
cv2.imshow("Original", image)
cv2.waitKey(0)
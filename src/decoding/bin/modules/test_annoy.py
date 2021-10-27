from annoy import AnnoyIndex
import numpy as np
from icecream import ic

image_array = np.array(([0.94,0,0], [0,0.68,0], [0, 0, 0.73]))
codebook = np.array(([1,0,0], [0, 1, 0], [0,0,1]))
_, n_cols = codebook.shape

f = len(codebook)
t = AnnoyIndex(f, 'euclidean')  # Length of item vector that will be indexed
for i in range(n_cols):
    v = codebook[i,:]
    t.add_item(i, v)

t.build(10) # 10 trees
t.save('test.ann')

# # ...

u = AnnoyIndex(f, 'euclidean')
u.load('test.ann') # super fast, will just mmap the file
for pixel in image_array:
    print(u.get_item_vector((u.get_nns_by_vector(pixel, 1, search_k=-1, include_distances=False))[0])) # This is a way to get the closest vector


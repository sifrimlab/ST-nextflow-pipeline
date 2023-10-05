import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob
from pyxelperfect.display import plotSpatial
from skimage import io
from skimage.color import *
from skimage.exposure import match_histograms

def overlay(img1, img2, img3):
    if isinstance(img1, str):
        img1 = io.imread(img1)    
    if isinstance(img2, str):
        img2 = io.imread(img2)
    # Normalize for visibility\n",
#     img1 = normalizeImg(img1)
#     img2 = normalizeImg(img2)
#     img3 = normalizeImg(img3)
    if img3 is None:
        img3 = np.zeros(img1.shape)

    zeros = np.zeros(img1.shape, dtype = img1.dtype)
#     img2 =  match_histograms(img2, img1)
#     img3 =  match_histograms(img3, img1)
    stacked = np.stack((img1, img2, img3), axis=2)
#     plt.imshow(stacked)
    return stacked

def normalizeImg(img):
    norm_image = (img - np.amin(img)) * (1.0 / (np.amax(img) - np.amin(img)))
    return norm_image


def channelnorm(im, channel, vmin, vmax, in_place=False):
    if not in_place:
        copy_im = im.copy()
    else:
        copy_im = im
    c = (copy_im[:,:,channel]-vmin) / (vmax-vmin)
    c[c<0.] = 0
    c[c>1.] = 1
    copy_im[:,:,channel] = c
    return copy_im

imgs =sorted(glob( "./fake_merfish_out_groupA/filtered/deconvolved//*.tif"))
# imgs_col =np.array( io.imread_collection(imgs))
# imgs_col = imgs_col.transpose(1, 2, 0)
imgs = [io.imread(img) for img in imgs]
# print(imgs[1].shape)
imgs = [img / np.amax(img) for img in imgs]
imgs[2] = match_histograms(imgs[2], imgs[0])
imgs[1] = match_histograms(imgs[1], imgs[0])

# # for img in imgs:
# #     plt.imshow(img,vmax=0.1)
#     # plt.show()

stacked = overlay(imgs[0], imgs[1], imgs[2])


vmin_dir = {0: 0, 1:0, 2:0}
vmax_dir  = {0: 0.1, 1:0.1, 2:0.1}
tmp_stacked = stacked.copy()
for channel in range(3):
    vmax = vmax_dir[channel]
    vmin = vmin_dir[channel]
    channelnorm(tmp_stacked, channel, vmin, vmax, in_place=True)

fig, axs = plt.subplots(1,2, sharex=True, sharey=True)
axs[0].imshow(tmp_stacked)
df = pd.read_csv("./fake_merfish_out_groupA/decoded/concat_decoded_genes.csv")
plotSpatial(tmp_stacked, df, rowname="Y", colname="X", color="Gene", dotsize=1, plot=False, ax=axs[1], colormap="Set1")
plt.show()






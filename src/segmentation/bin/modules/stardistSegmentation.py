from __future__ import print_function, unicode_literals, absolute_import, division
from stardist.models import StarDist2D
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from tifffile import imread
from csbdeep.utils import Path, normalize
from csbdeep.io import save_tiff_imagej_compatible
from stardist import random_label_cmap, _draw_polygons, export_imagej_rois
from stardist.models import StarDist2D

np.random.seed(6)
lbl_cmap = random_label_cmap()

# save_tiff_imagej_compatible('example_image.tif', img, axes='YX')
# save_tiff_imagej_compatible('example_labels.tif', labels, axes='YX')
# export_imagej_rois('example_rois.zip', details['coord'])
X = sorted(glob('/media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/results/tiled_DO/DAPI_*.tif'))
X = list(map(imread,X))

def segment(img, model, show_dist=True):
    # extract number of channels in case the input image is an RGB image
    n_channel = 1 if X[0].ndim == 2 else X[0].shape[-1]
    # depending on that, we want to normalize the channels independantly
    axis_norm = (0,1)   # normalize channels independently
    # axis_norm = (0,1,2) # normalize channels jointly
    img = normalize(img, 1,99.8, axis=axis_norm)
    plt.imshow(img)
    plt.show()
    labels, details = model.predict_instances(img)

    plt.figure(figsize=(13,10))
    img_show = img if img.ndim==2 else img[...,0]
    coord, points, prob = details['coord'], details['points'], details['prob']
    plt.subplot(121); plt.imshow(img_show, cmap='gray'); plt.axis('off')
    a = plt.axis()
    _draw_polygons(coord, points, prob, show_dist=show_dist)
    plt.axis(a)
    plt.subplot(122); plt.imshow(img_show, cmap='gray'); plt.axis('off')
    plt.imshow(labels, cmap=lbl_cmap, alpha=0.5)
    plt.tight_layout()
    plt.show()

# versatile model
model_versatile = StarDist2D.from_pretrained('2D_versatile_fluo')
example(model_versatile, 1, False)


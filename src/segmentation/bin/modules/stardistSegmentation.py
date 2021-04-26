from __future__ import print_function, unicode_literals, absolute_import, division
import numpy as np
from glob import glob
from skimage import io
import pandas as pd
from csbdeep.utils import Path, normalize
from csbdeep.io import save_tiff_imagej_compatible
from stardist import random_label_cmap, _draw_polygons, export_imagej_rois
from stardist.models import StarDist2D

# np.random.seed(6)
# lbl_cmap = random_label_cmap()

# save_tiff_imagej_compatible('example_image.tif', img, axes='YX')
# save_tiff_imagej_compatible('example_labels.tif', labels, axes='YX')
# export_imagej_rois('example_rois.zip', details['coord'])

def segment(img_path,model, show_dist=True):
    img = io.imread(img_path)
    # extract number of channels in case the input image is an RGB image
    n_channel = 1 if img.ndim == 2 else img.shape[-1]
    # depending on that, we want to normalize the channels independantly
    axis_norm = (0,1)   # normalize channels independently
    # axis_norm = (0,1,2) # normalize channels jointly

    img_normalized = normalize(img, 1,99.8, axis=axis_norm)
    labels, details = model.predict_instances(img_normalized)
    coord, points, prob = details['coord'], details['points'], details['prob']

    attribute_df = pd.DataFrame()
    attribute_df['Y'] = points[:,0]
    attribute_df['X'] = points[:,1]
    attribute_df['prob'] = prob

    # print(points.shape, coord.shape,prob.shape )
    return labels, attribute_df

if __name__=='__main__':
    image_path = "/media/tool/gabriele_data/1442_OB/maxIP-seperate-channels/results_minsigma2_maxsigma20/tiled_DO/DAPI_padded_tiled_29.tif"
    model_versatile = StarDist2D.from_pretrained('2D_versatile_fluo')
    segment(image_path, model_versatile)

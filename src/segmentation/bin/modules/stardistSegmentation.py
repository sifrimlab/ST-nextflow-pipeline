from __future__ import print_function, unicode_literals, absolute_import, division
import numpy as np
from glob import glob
from skimage import io
from skimage import measure
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

def segment(img,model, show_dist=True):
    # extract number of channels in case the input image is an RGB image
    n_channel = 1 if img.ndim == 2 else img.shape[-1]
    # depending on that, we want to normalize the channels independantly
    axis_norm = (0,1)   # normalize channels independently
    # axis_norm = (0,1,2) # normalize channels jointly

    img_normalized = normalize(img, 1,99.8, axis=axis_norm)
    labeled_image, details = model.predict_instances(img_normalized)
    # coord, points, prob = details['coord'], details['points'], details['prob']

    # attribute_df = pd.DataFrame()
    # attribute_df['Y'] = points[:,0]
    # attribute_df['X'] = points[:,1]
    # attribute_df['prob'] = prob
    return labeled_image #, attribute_df

def getProperties(labeled_image, dapi_image):
    regions = measure.regionprops(labeled_image, intensity_image=dapi_image)
    pixels_to_um = 0.454 # 1 pixel = 454 nm (got this from the metadata of original image)
    propList = ['Area',
                'equivalent_diameter', 
                'orientation', 
                'MajorAxisLength',
                'MinorAxisLength',
                'Perimeter',
                'MinIntensity',
                'MeanIntensity',
                'MaxIntensity']    

    rows_list=[]
    for region_props in regions:
        attribute_dict = {}
        attribute_dict['Image_Label'] =region_props['Label']
        center_y, center_x= region_props['centroid']
        attribute_dict['Cell_Label'] = f"X{int(center_x)}_Y{int(center_y)}_{region_props['Label']}"
        attribute_dict['Center_X'] = int(center_x)
        attribute_dict['Center_Y'] = int(center_y)
        for i,prop in enumerate(propList):
            if(prop == 'Area'): 
                attribute_dict['area'] = region_props[prop]*pixels_to_um**2 
            elif(prop == 'orientation'): 
                attribute_dict['orientation'] = region_props[prop]*57.2958
            elif(prop.find('Intensity') < 0):          # Any prop without Intensity in its name
                attribute_dict[prop] = region_props[prop]*pixels_to_um
            else: 
                attribute_dict[prop] = region_props[prop]
        rows_list.append(attribute_dict)
    attribute_df = pd.DataFrame(rows_list)
    return attribute_df

if __name__=='__main__':
    # image_path = "/media/tool/gabriele_data/1442_OB/maxIP-seperate-channels/results_minsigma2_maxsigma20/tiled_DO/DAPI_padded_tiled_29.tif"
    image_path ="/media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/DO/DAPI.TIF" 
    model_versatile = StarDist2D.from_pretrained('2D_versatile_fluo')
    labeled_image, attribute_df1 = segment(image_path, model_versatile)
    dapi_image = io.imread(image_path)
    attibute_df2 = getProperties(labeled_image, dapi_image)
    attribute_df1.to_csv("1.csv")
    attibute_df2.to_csv("2.csv")


import cv2
import re
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage
from skimage import measure, color, io
from skimage.util import img_as_ubyte 
from icecream import ic


def collectProperties(property_csv_list: str):
    """
    The idea here is to concat all labels of different tiles, and give them a unique label number, because this will not be the case
    """
    df_list = [pd.read_csv(csv) for csv in property_csv_list]
    total_df = pd.concat(df_list)
    total_df = total_df.sort_values(by=['Tile'])
    new_index = list(range(1,len(total_df)+1))
    total_df['Label'] = new_index
    return total_df

def otsuThresholding(path_to_image: str, tile_nr=""):
    '''
        note to self: this code adapted from DigitalSreeni assumes that your input image is an 8-bit rgb, which makes it so that we have to do some image format transformation because:
        - cv2.shreshold accepts only 8-bit grayscale
        - cv2.watershed only accepts 8-bit rgb
    '''
    '''
    returns a labeled image, where 0 = background and all other integers an object number. 
    These numbers don't have any actual image value, so the image isn't really used as an image object, but more as an array
    that stores which pixel belongs to which label. Also returns a csv that contains image properties of the given objects
    '''
    img =io.imread(path_to_image) 
    # Extract tile number for umi's later on
    # Create an 8bit version of the image
    img_as_8 = img_as_ubyte(img)
    # Creat an RGB version that only has signal in the blue channel
    shape = img_as_8.shape
    empty = np.zeros(shape)
    img_as_8bit_RGB = cv2.merge([img_as_8,img_as_8,img_as_8])

    try:
        cells = img[:,:,0]
    except IndexError:
        cells = img_as_8
    

    pixels_to_um = 0.454 # 1 pixel = 454 nm (got this from the metadata of original image)

    ret1, thresh = cv2.threshold(cells, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # Morphological operations to remove small noise - opening
    #To remove holes we can use closing
    kernel = np.ones((3,3),np.uint16)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

    # from skimage.segmentation import clear_border
    # opening = clear_border(opening) #Remove edge touching grains

    sure_bg = cv2.dilate(opening,kernel,iterations=10)
    dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
    ret2, sure_fg = cv2.threshold(dist_transform,0.5*dist_transform.max(),255,0)

    #Later you realize that 0.25* max value will not separate the cells well.
    #High value like 0.7 will not recognize some cells. 0.5 seems to be a good compromize

    # Unknown ambiguous region is nothing but bkground - foreground
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)

    #Now we create a marker and label the regions inside. 
    # For sure regions, both foreground and background will be labeled with positive numbers.
    # Unknown regions will be labeled 0. 
    #For markers let us use ConnectedComponents. 
    ret3, markers = cv2.connectedComponents(sure_fg)

    #One problem rightnow is that the entire background pixels is given value 0.
    #This means watershed considers this region as unknown.
    #So let us add 10 to all labels so that sure background is not 0, but 10
    markers = markers+10

    # Now, mark the region of unknown with zero
    markers[unknown==255] = 0

    #Now we are ready for watershed filling. 
    markers = cv2.watershed(img_as_8bit_RGB,markers)
    #The boundary region will be marked -1
    markers[markers==-1] = 10 # add the boundary images to the background
    label_image = measure.label(markers, background=10)

    ## Extract properties of detected cells
    regions = measure.regionprops(label_image, intensity_image=img)

    #Best way is to output all properties to a csv file
    #Let us pick which ones we want to export. 

    propList = ['Area',
                'equivalent_diameter', #Added... verify if it works
                'orientation', #Added, verify if it works. Angle btwn x-axis and major axis.
                'MajorAxisLength',
                'MinorAxisLength',
                'Perimeter',
                'MinIntensity',
                'MeanIntensity',
                'MaxIntensity']    

    # output_file = open('cell_measurements.csv', 'w')
    # output_file.write(',' + ",".join(propList) + '\n') #join strings in array by commas, leave first cell blank

    rows_list=[]
    for region_props in regions:
        attribute_dict = {}
        center_y, center_x= region_props['centroid']
        attribute_dict['Image_Label'] =region_props['Label']
        attribute_dict['Cell_Label'] = f"T{tile_nr}_X{int(center_x)}_Y{int(center_y)}_{region_props['Label']}"
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
    return label_image, attribute_df



if __name__=='__main__':
    image_path = "/media/david/Puzzles/gabriele_data/1442_OB/DO/DAPI.tif"
    original_image = io.imread(image_path)
    cut_image = original_image[3000:5000, 2000:4000]
    # cut_image_8bit = img_as_ubyte(cut_image)
    io.imsave("test.tif", cut_image)
    label_image, attribute_df = otsuThresholding("test.tif")
    colored_image = color.label2rgb(label_image, bg_label=0) 
    fig, axs = plt.subplots(1,2)
    axs[0].imshow(colored_image)
    axs[1].imshow(cut_image)
    plt.show()


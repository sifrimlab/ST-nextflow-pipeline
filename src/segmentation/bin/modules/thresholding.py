import cv2
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage
from skimage import measure, color, io
from icecream import ic

def otsuThresholding(path_to_image: str):
    '''
    returns a labeled image, where 0 = background and all other integers an object. also returns a csv that contains image properties of the given objects
    '''
    img = cv2.imread(path_to_image)
    cells = img[:,:,0]
    pixels_to_um = 0.454 # 1 pixel = 454 nm (got this from the metadata of original image)

    ret1, thresh = cv2.threshold(cells, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # cv2.imwrite("otsu_thresh.png",thresh)

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
    markers = cv2.watershed(img,markers)
    #The boundary region will be marked -1
    markers[markers==-1] = 10 # add the boundary images to the background
    label_image = measure.label(markers, background=10)

    ## Extract properties of detected cells
    regions = measure.regionprops(label_image, intensity_image=cells)

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
        attribute_dict['Label'] = region_props['Label'] 
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
    otsuThresholding("/media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/DO/DAPI.TIF")

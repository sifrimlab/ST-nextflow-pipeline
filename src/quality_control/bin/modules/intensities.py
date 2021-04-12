from skimage import io
from icecream import ic
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

def getHistogram(path_to_image):
    image = cv2.imread(path_to_image, 0)
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    return hist
   # plt.plot(hist)
   # plt.xlim([0, 256])
   # plt.show()

def plotHistograms(hist_dict):
    # Extract names
    names=list(hist_dict.keys())
    # Extract histograms, and cast to histograms if they are not already
    hist_list = list(hist_dict.values())
    hist_list = [getHistogram(value)  if isinstance(value, str) else value for value in hist_list]
    
    # start with one figure.
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(hist_list[0])
    ax.set_title(names[0])
    ax.set_xlabel("pixel value")
    ax.set_ylabel("# times encountered")
    # Then plot more as they pass by the forloop, each time updating the axes geometry
    for i in range(0,len(names)):
        if i==0:
            continue

        n = len(fig.axes)
        for j in range(n):
            fig.axes[j].change_geometry(n+1, 1, j+1)
        
        # add the new
        ax = fig.add_subplot(n+1, 1, n+1)
        ax.plot(hist_list[i])
        ax.set_title(names[i])
        ax.set_xlabel("pixel value")
        ax.set_ylabel("# times encountered")
    return plt


def getPeaks(hist):
    hist = hist[:,0]
    peaks, properties = find_peaks(hist)
    peak_values = [hist[i] for i in peaks]
    # create a dict with peak_values being the key, peaks being the value
    peak_dict = {peak_value: peak for peak, peak_value in zip(peaks, peak_values)}
    temp_peak_values = list(peak_dict.keys())
    first_max = int(max(temp_peak_values))
    temp_peak_values.remove(first_max)
    second_max =int(max(temp_peak_values))

    first_max_pixel_value = peak_dict[first_max]
    second_max_pixel_value = peak_dict[second_max]
    first_max_tuple = (first_max_pixel_value, first_max)    
    second_max_tuple = (second_max_pixel_value, second_max)   

    return first_max_pixel_value, second_max_pixel_value

def getAverageIntensity(hist):
    hist = hist.astype(int)
    temp = np.insert(hist, 0,range(1,257), axis=1)
    average = np.average(temp[:,0], weights=temp[:,1])
    return average

# Return a dict with key = image name, value is a dict with key=attribute, value= value of that attribute
def getIntensityAnalytics(name: str, hist):
    hist = hist.astype(int)
    average = getAverageIntensity(hist)
    first_max_peak, second_max_peak = getPeaks(hist)
    hist_2D = np.insert(hist, 0,range(0,256), axis=1)
    without_zero_values = np.copy(hist_2D)
    # Remove all row's that have a zero in the second column
    without_zero_values = without_zero_values[without_zero_values[:,1]!=0,:]
    minimum_pixel_value = min(without_zero_values[:,0])
    maximum_pixel_value = max(without_zero_values[:,0])
    


    # Creating the dicst of attributes:
    attribute_dict = {}
    attribute_dict['image_name']=name
    attribute_dict['minimum_pixel_value']=int(minimum_pixel_value)
    attribute_dict['maximum_pixel_value']=int(maximum_pixel_value)
    attribute_dict['first_peak']=int(first_max_peak)
    attribute_dict['second_peak']=int(second_max_peak)
    attribute_dict['average_intensity']=int(average)
    return attribute_dict

def collectIntensityAnalytics(rows_list):
    df = pd.DataFrame.from_dict(rows_list)  
    df = df.sort_values(by=['image_name'])
    return  df  

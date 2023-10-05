from skimage import io
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random # for random color plotting
from skimage import io
from skimage.util import img_as_ubyte
from scipy.signal import find_peaks

def getHistogram(path_to_image):
    image = io.imread(path_to_image)
    image = img_as_ubyte(image)
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    return hist

def plotCombinedHistograms(hist_dict, title = ""):
    def getRandomColor():
        r = random.random()
        g = random.random()
        b = random.random()
        color = (r,g,b)
        return color

    fig, ax = plt.subplots(1,1)
    ax.set_title(title)
    ax.set_xlabel("8-bit grayscale pixel value")
    ax.set_ylabel("# times encountered")

    for name, hist in hist_dict.items():
        ax.plot(hist, color=getRandomColor(), label=name)
    ax.legend()
    return plt

def plotHistograms(hist_dict):
    # Extract names
    names=list(hist_dict.keys())
    # Extract histograms, and cast to histograms if they are not already
    hist_list = list(hist_dict.values())
    hist_list = [getHistogram(value)  if isinstance(value, str) else value for value in hist_list]
    def getRandomColor():
        r = random.random()
        g = random.random()
        b = random.random()
        color = (r,g,b)
        return color
    # start with one figure.
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(hist_list[0], color=getRandomColor())
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
        ax.plot(hist_list[i], getRandomColor())
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

    # Create a list of the peak values to find the maxima
    temp_peak_values = list(peak_dict.keys())
    first_max = int(max(temp_peak_values))
    temp_peak_values.remove(first_max)
    second_max =int(max(temp_peak_values))

    first_max_pixel_value = peak_dict[first_max]
    second_max_pixel_value = peak_dict[second_max]
    first_max_tuple = (first_max_pixel_value, first_max)    
    second_max_tuple = (second_max_pixel_value, second_max)   

    return first_max_pixel_value, first_max, second_max_pixel_value, second_max

def getAverageIntensity(hist):
    hist = hist.astype(int)
    temp = np.insert(hist, 0,range(1,257), axis=1)
    average = np.average(temp[:,0], weights=temp[:,1])
    return average

# Return a dict with key = image name, value is a dict with key=attribute, value= value of that attribute
def getIntensityAnalytics(name: str, image_path: str, hist ):
    attribute_dict = {}
    hist = hist.astype(int)
    image = io.imread(image_path)
    image = img_as_ubyte(image)
    n_pixels = np.sum(hist)
    # Get average intensity pixel value weighted by the number of times counted
    average = getAverageIntensity(hist)
    # Get peak information
    first_max_pixel_value, first_max, second_max_pixel_value, second_max= getPeaks(hist) 
    try:
        n_pixels_lower_than_first_peak = np.sum(np.where(image <= first_max_pixel_value, 1,0))
        median_of_pixel_values = (first_max_pixel_value+second_max_pixel_value)/2

        n_pixels_lower_than_median_value = np.sum(np.where(image<= median_of_pixel_values, 1,0))
        percentage_lower_than_first_peak = (n_pixels_lower_than_first_peak/n_pixels)*100
        percentage_lower_than_medium = (n_pixels_lower_than_median_value/n_pixels)*100
        attribute_dict['median_pixel_value']=median_of_pixel_values
        attribute_dict['percentage_lower_than_first_peak']= percentage_lower_than_first_peak
        attribute_dict['percentage_lower_than_medium']= percentage_lower_than_medium
    except: 
        pass

    # Get min and max pixel value by removing pixel values that didn't have a pixel counted
    hist_2D = np.insert(hist, 0,range(0,256), axis=1)
    without_zero_values = np.copy(hist_2D)
    # Remove all row's that have a zero in the second column
    without_zero_values = without_zero_values[without_zero_values[:,1]!=0,:]
    minimum_pixel_value = min(without_zero_values[:,0])
    maximum_pixel_value = max(without_zero_values[:,0])
    
    # Creating the dicst of attributes:
    attribute_dict['image_name']=name
    attribute_dict['minimum_pixel_value']=int(minimum_pixel_value)
    attribute_dict['maximum_pixel_value']=int(maximum_pixel_value)
    attribute_dict['first_peak']=int(first_max_pixel_value)
    attribute_dict['# pixels_in_first_peak']=int(first_max)
    attribute_dict['second_peak']=int(second_max_pixel_value)
    attribute_dict['# pixels_in_second_peak']=int(second_max)
    attribute_dict['average_intensity']=int(average)
    return attribute_dict

def collectIntensityAnalytics(rows_list):
    df = pd.DataFrame.from_dict(rows_list)  
    df = df.sort_values(by=['image_name'])
    return  df  

if __name__ == '__main__':
    # this is to plot the histogram of hippo_3 manually
    img_list = [f"/media/tool/gabriele_data/161230_161220_3_1/maxIP-seperate-channels/Round1/Round1_c{i}_maxIP.tif" for i in range(1,5)]
    names = [f"Round1-Channel{i}" for i in range(1,5)]
    histograms = {name: getHistogram(image_path) for name, image_path in zip(names, img_list)}
    plt = plotCombinedHistograms(hist_dict=histograms)
    plt.savefig("/media/nacho/Puzzles/results_figures/hippo_3_quality_report_zoomed.png")


    # img_list = [f"/media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/Round1/Round1_c{i}.TIF" for i in range(2,6)]
    # hist_dict = {i: getHistogram(img) for i,img in enumerate(img_list)}

    # plotCombinedHistograms(hist_dict)

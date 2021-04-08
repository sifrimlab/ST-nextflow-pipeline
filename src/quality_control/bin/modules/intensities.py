from skimage import io
from icecream import ic
import cv2
import matplotlib.pyplot as plt
import numpy as np

def getHistogram(path_to_image):
    image = cv2.imread(path_to_image, 0)
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    return hist
   # plt.plot(hist)
   # plt.xlim([0, 256])
   # plt.show()

def plotHistograms(histogram_list):
    number_of_hists=len(histogram_list)

    # start with one
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(histogram_list[0])
    # Then plot more as they pass by the forloop, each time updating the axes geometry
    for i, hist in enumerate(histogram_list):
        if i==0:
            continue

        n = len(fig.axes)
        for j in range(n):
            fig.axes[j].change_geometry(n+1, 1, j+1)
        
        # add the new
        ax = fig.add_subplot(n+1, 1, n+1)
        ax.plot(hist)
        
    plt.show()

def assesAverageIntensity(histogram_list):
    average_list = []
    for hist in histogram_list:
        hist = hist.astype(int)
        temp = np.insert(hist, 0,range(1,257), axis=1)
        average = np.average(temp[:,0], weights=temp[:,1])
        average_list.append(average)
        return average_list
def checkIfEmpty(path_to_image):
    image = io.imread(path_to_image)
    result = np.all((image == 0))
    return result
    
images = [f"/media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/Round1/c{i}.TIF" for i in range(2,6)]
hist_list=[]
for image in images:
    hist_list.append(getHistogram(image))
assesAverageIntensity(hist_list)

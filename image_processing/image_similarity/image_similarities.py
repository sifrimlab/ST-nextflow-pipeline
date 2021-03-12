'''
    This python document contains different kinds of helper functions to quickly determine different kinds of similarity measurements 
    between two images in multiple heuristic ways.
'''

from skimage.io import imread
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error

import cv2 
from icecream import ic

def getHistogram(pathToImage):
    ##Works with grayscale, so only focuses on intensity, which is a good thing for ISS data so far I believe
    ##Working with histograms completely ignores the spatial aspect of all of this though, so for image registration problem detection this might not be the most useful thing just yet
    image = cv2.cv2.imread(pathToImage) 
    gray_image = cv2.cv2.cvtColor(image, cv2.cv2.COLOR_BGR2GRAY) 
    histogram = cv2.cv2.calcHist([gray_image], [0],  None, [256], [0, 256])
    return histogram


def SimilarHistogram(pathToReferenceImage, pathToImage1, pathToImage2):
    #reference
    histogram = getHistogram(pathToReferenceImage) 
    
    #Image1 image 
    histogram1 = getHistogram(pathToImage1)
    
    # data2 image 
    histogram2 = getHistogram(pathToImage2) 

    c1 = 0
    c2= 0
    # Euclidean Distace between first image and test 
    i = 0
    while i<len(histogram) and i<len(histogram1): 
        c1+=(histogram[i]-histogram1[i])**2
        i+= 1
    c1 = c1**(1 / 2) 
    
    # Euclidean Distace between second image and reference 
    i = 0
    while i<len(histogram) and i<len(histogram2): 
        c2+=(histogram[i]-histogram2[i])**2
        i+= 1
    c2 = c2**(1 / 2) 
    
    if(c1<c2): 
        print("Image 1 is more similar to the reference as compared to image 2") 
    else: 
        print("Image 2 is more similar to the reference as compare to Image 1") 

def EuclideanImageSimilarity(pathToImage1, pathToImage2):
    hist1 = getHistogram(pathToImage1)
    hist2 = getHistogram(pathToImage2)
    distance=0
    i=0
    while i<len(hist1) and i<len(hist2): 
        distance+=(hist1[i]-hist2[i])**2
        i+= 1
    distance = distance**(1 / 2)   
    return(distance)

def MeanSquaredErrorImageSimilarity(pathToImage1, pathToImage2):
    #image needs to be a numpy.ndarray
    img1 = imread(pathToImage1)
    img2 = imread(pathToImage2)
    mse = mean_squared_error(img1, img2)
    return mse

def StructuralSimilarity(pathToImage1, pathToImage2):
    img1 = imread(pathToImage1)
    img2 = imread(pathToImage2)
    sim = ssim(img1, img2)
    return sim

def ORBsimilarity(pathToImage1, pathToImage2, threshold):
    if not (0<threshold<100):
        raise ValueError("Threshold is not between 0 and 100")
    ## This basically detects keypoints and then counts how many keypoints are less than a certain distance seperated from eachother based on a threshold
    orb = cv2.cv2.ORB_create()
    img1 = cv2.cv2.imread(pathToImage1)
    img2 = cv2.cv2.imread(pathToImage2)
  # detect keypoints and descriptors
    kp_a, desc_a = orb.detectAndCompute(img1, None)
    kp_b, desc_b = orb.detectAndCompute(img2, None)
    # define the bruteforce matcher object
    bf = cv2.cv2.BFMatcher(cv2.cv2.NORM_HAMMING, crossCheck=True)
        
    #perform matches. 
    matches = bf.match(desc_a, desc_b)
    #Look for similar regions with distance < 50. Goes from 0 to 100 so pick a number between.
    similar_regions = [i for i in matches if i.distance < 50]  
    if len(matches) == 0:
        return 0
    return len(similar_regions) / len(matches)


def MahalanobisDistance(pathToImage1, pathToImage2):
    #TODO implement 
    return None
import cv2
import os
from PIL import Image
from resolution_check import getResolution
import math
from icecream import ic

def pad(filepath, width, height, expectedWidth=0, expectedHeight=0):
    #returns an openCV image, probably to be saved by imwrite by the caller

    #Note hare that i use ceil to round up, this might cause some unwanted behaviour in the future.
    #combine with getResolution() to check for any problems regularly
    currentWidth, currentHeight = getResolution(filepath)

    widthToAdd = math.floor((width - currentWidth)/2)
    heightToAdd = math.floor((height - currentHeight)/2)
    img = cv2.cv2.imread(filepath, cv2.cv2.IMREAD_ANYDEPTH)
    #In case there is still a difference in pixels to add and the wanted resolution, add that difference to the right or top,
    # depending on whether the difference is in width or in height respectively
    differenceWidth = (width-currentWidth) - widthToAdd*2
    differenceHeight = (height-currentHeight) - heightToAdd*2
    paddedImage = cv2.cv2.copyMakeBorder(img, heightToAdd+differenceHeight, heightToAdd, widthToAdd, widthToAdd+differenceWidth, cv2.cv2.BORDER_CONSTANT)
    newHeight = paddedImage.shape[0]
    newWidth = paddedImage.shape[1]
    if expectedHeight == 0 or expectedWidth == 0:
        pass
    else:
        if expectedWidth != newWidth:
            print("Warning: Width of resulting padded image is not equal to the entered expected width")
        if expectedHeight != newHeight:
            print("Warning: Height of resulting padded image is not equal to the entered expected height")
    return paddedImage 


##calculating the largest resolution 

# largestWidth = 0
# largestHeight = 0
# for i in range(1,7):
#     os.chdir(f"/media/tool/spatial1/starfish_format/{i}")
#     for filename in os.listdir(os.getcwd()):
#         width, height = getResolution(filename)
#         if width > largestWidth:
#             largestWidth = width
#         if height > largestHeight:
#             largestHeight = height
# os.chdir("/media/tool/spatial1/starfish_format/DO")
# for filename in os.listdir(os.getcwd()):
#         width, height = getResolution(filename)
#         if width > largestWidth:
#             largestWidth = width
#         if height > largestHeight:
#             largestHeight = height


##using the largest resolution to pad images:


# for i in range(1,7):
#     os.chdir(f"/media/tool/spatial1/starfish_format/{i}")
#     os.mkdir(f"/media/tool/spatial1/starfish_format/padded/{i}")
#     for filename in os.listdir(os.getcwd()):     
#         paddedImage = pad(filename, largestWidth, largestHeight, expectedWidth=9420, expectedHeight=25959)
#         cv2.cv2.imwrite(f"/media/tool/spatial1/starfish_format/padded/{i}/{filename}",paddedImage)
# os.chdir("/media/tool/spatial1/starfish_format/DO")
# os.mkdir("/media/tool/spatial1/starfish_format/padded/DO")
# for filename in os.listdir(os.getcwd()):
#     paddedImage = pad(filename, largestWidth, largestHeight, expectedWidth=9420, expectedHeight=25959)
#     cv2.cv2.imwrite(f"/media/tool/spatial1/starfish_format/padded/DO/{filename}",paddedImage)
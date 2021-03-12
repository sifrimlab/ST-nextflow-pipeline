# importing the module 
import os
from PIL import Image
##important for giant tiff files, otherwise PIL thinks it's malware
 ##obviously this is removing some security, so make sure you don't open a cyberpunk update or something
Image.MAX_IMAGE_PIXELS = None
import cv2
from icecream import ic

def getResolution(filepath):
    im = Image.open(filepath)
    width, height = im.size
    return width, height

# loading the image 
# for i in range(1,7):
#     os.chdir(f"/media/tool/spatial1/starfish_format/padded/{i}")
#     for filename in os.listdir(os.getcwd()):
#         w, h = getResolution(filename)
#         # displaying the dimensions 
#         print(str(i) + "\t" + str(filename) + "\t" + str(w) + "x" + str(h))


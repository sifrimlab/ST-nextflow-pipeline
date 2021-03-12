import os
import cv2
from crop_image import crop


if __name__ == __name__:
    for i in range(1,7):
        os.chdir(f"T:\\spatial1\\starfish_format\\{i}")
        os.mkdir(f"T:\\spatial1\\starfish_format\\resolution_fixing\\test\\{i}")
        for filename in os.listdir(os.getcwd()):
            crop(filename, 6758,22397, f"T:\\spatial1\\starfish_format\\resolution_fixing\\test\\{i}")
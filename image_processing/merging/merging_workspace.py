import os
from merge_images import createComposite
import cv2
ref_tif_files_dict = {}
round_tif_files_dict = {}

imgpath = "/home/nacho/Documents/Code/image_processing/image_similarity/imgs"

for file in os.listdir(imgpath):
    if file.endswith(".tif"):
        try:
            number = file.split(".")[0].split("_tile")[1]
            prefix = file.split("_")[0]
            if prefix == "ref":
                ref_tif_files_dict[number] = file
            elif prefix == "registered":
                round_tif_files_dict[number]=file
        except:
            pass

for k,v in ref_tif_files_dict.items():
    cv2.imwrite(f"composite_{k}.tif", createComposite(v, round_tif_files_dict[k]))
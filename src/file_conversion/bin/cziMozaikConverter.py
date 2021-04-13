import numpy as np
import aicspylibczi
import os
from PIL import Image
from skimage import io
import sys

def maxIPstack(img_list):
    parsed_list = img_list
    parsed_list = [img if isinstance(img, np.ndarray) else io.imread(img) for img in img_list]
    # now all elements in parsed_list are ndarrays
    maxIP = np.maximum.reduce(parsed_list)
    return maxIP

def writeMozaicImages(czi_image, channel_nr,output_prefix=""):
    channel_index = channel_nr-1 # Indexing in czi api is 0 based, but user will be thinking in 1 based indexing.
    z_stack_min, z_stack_max = czi_image.dims_shape()[0]['Z'] #unpack the necessary 
    image_list = []
    for i in range(z_stack_min, z_stack_max):
        mosaic_data = czi_image.read_mosaic(C=channel_index, Z=i, scale_factor=1)
        mosaic_data = mosaic_data[0,0,:,:].astype(np.uint16)
        image_list.append(mosaic_data)
    maxIP = maxIPstack(image_list)
    output_filename= f"{ output_prefix }_c{channel_nr}.tif"
    io.imsave(output_filename, maxIP)


filepath = sys.argv[1]
prefix = os.path.splitext(filepath)[0]

# if a third argument is inputted, it should be teh dir where the user want the files stored, otherwise the code will assume this is part of an entire workflow and just write to cwd.

czi = aicspylibczi.CziFile(filepath)
c_stack_min, c_stack_max = czi.dims_shape()[0]['C']
for i in range(c_stack_min+1, c_stack_max+1): # I want them named starting at 1, not at 0
    writeMozaicImages(czi_image=czi, channel_nr=i,  output_prefix=prefix)

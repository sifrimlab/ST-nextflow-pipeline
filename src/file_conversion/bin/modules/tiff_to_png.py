from skimage import io
from skimage import exposure
import cv2
import os


def convertTiffToPng(tiff_image_path: str, prefix, output_dir = ""):
    image = io.imread(tiff_image_path)
    adapthist = exposure.equalize_adapthist(image)
    io.imsave(f"{os.path.join(output_dir, prefix)}.png", adapthist)


for dir in os.listdir(os.getcwd()):
      for file in os.listdir(dir):
        if "tiled_29" in file:
            if file.endswith(".tif"):
                convertTiffToPng(f"{dir}/{file}", file, "/media/Puzzles/gabriele_data/1442_OB/tile_29/")


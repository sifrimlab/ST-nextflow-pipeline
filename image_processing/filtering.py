import os
import cv2
import sys
from skimage.morphology import white_tophat
from skimage import io
# from inputParsing import makeDir


# def writeFilteredImages(tiled_dataframe, output_dir):
#     """Filters all images in the dataframe with white tiphat, and writes the resulting images into a new folder output dir

#     Parameters
#     ----------
#     tiled_dataframe : pandas DataFrame
#         Input dataframe that contains the paths to the images to be filtered
#     output_dir : [type]
#         Target directory where the filtered images will be written to.
#     """
#     for row in tiled_dataframe.itertuples():
#         round_path = os.path.join(output_dir, f"Round{str(row.Round)}") + "/"
#         file_name = row.Image_path.split("/")[-1]
#         ref_name = row.Reference.split("/")[-1]
#         dapi_name = row.DAPI.split("/")[-1]
#         makeDir(round_path)
#         cv2.imwrite(os.path.join(round_path, file_name), white_tophat(cv2.imread(row.Image_path)))
#         if not os.path.isfile(os.path.join(round_path, ref_name)):
#             cv2.imwrite(os.path.join(round_path, ref_name), white_tophat(cv2.imread(row.Reference)))
#         if not os.path.isfile(os.path.join(round_path, dapi_name)):
#             cv2.imwrite(os.path.join(round_path, dapi_name), white_tophat(cv2.imread(row.DAPI)))

#         print(f"Filtered images of tile {row.Tile} written to {round_path}")

def filterWithWhiteTophat(image):
    """Wrapper for skimage's white tophat filter

    Parameters
    ----------
    image : np.ndarray
        Image to be filtered.
    """
    return white_tophat(image)

img = io.imread(sys.argv[1])
prefix = os.path.splitext(sys.argv[1])
io.imsave(f"{prefix}.tif", filterWithWhiteTophat(img))
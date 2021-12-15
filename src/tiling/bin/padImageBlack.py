import sys
import os
from skimage import io
from modules.adaptedTileFunction import padImage
# important for giant tiff files, otherwise PIL thinks it's malware

image = sys.argv[1]
prefix = os.path.splitext(image)[0]
target_x = int(sys.argv[2])
target_y = int(sys.argv[3])

image_padded = padImage(image, target_full_rows = target_y, target_full_columns = target_x)
io.imsave(f"{prefix}_padded.tif", image_padded)

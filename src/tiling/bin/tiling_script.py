import sys
import os
from modules.adaptedTileFunction import tileImage


image = sys.argv[1]
prefix = os.path.splitext(image)[0]
xdiv = int(sys.argv[2])
ydiv = int(sys.argv[3])
tileImage(image_path = image,xdiv = xdiv, ydiv = ydiv,  image_prefix = prefix)

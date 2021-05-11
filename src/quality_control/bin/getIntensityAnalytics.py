from modules.intensities import getIntensityAnalytics, getHistogram
import sys
import os
import json
image_path = sys.argv[1]
prefix = os.path.splitext(image_path)[0]
image_analytics_dict = getIntensityAnalytics(prefix, image_path, getHistogram(image_path))
with open(f"{prefix}_intensity_analytics.json", "a+") as jsonfile:
    json.dump(image_analytics_dict, jsonfile)

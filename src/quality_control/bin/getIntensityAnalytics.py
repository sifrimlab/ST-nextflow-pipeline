from modules.intensities import getIntensityAnalytics, getHistogram
import sys
import os
import json
image = sys.argv[1]
prefix = os.path.splitext(image)[0]
image_analytics_dict = getIntensityAnalytics(prefix, getHistogram(image))
with open(f"{prefix}_intensity_analytics.json", "a+") as jsonfile:
    json.dump(image_analytics_dict, jsonfile)
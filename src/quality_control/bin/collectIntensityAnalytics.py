import sys
import pandas as pd
import json
from modules.intensities import collectIntensityAnalytics

json_list = [sys.argv[i] for i in range(1, len(sys.argv))]
dict_list = []
for json_path in json_list:
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
        dict_list.append(data)
df = collectIntensityAnalytics(dict_list)
df.to_html(open("combined_intensity_analytics.html", 'w'))


        
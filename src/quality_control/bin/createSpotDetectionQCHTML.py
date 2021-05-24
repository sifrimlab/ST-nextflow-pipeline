import json
from bs4 import BeautifulSoup
import pandas as pd
import sys

argument_index = 1
template = sys.argv[argument_index]
argument_index +=1

recall_json = sys.argv[argument_index]
argument_index +=1

precision_jsons_list = [sys.argv[i] for i in range(argument_index, len(sys.argv))]

precision_rows_list = []
# convert jsons back to dicts for html conversion
for json_path in precision_jsons_list:
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
        precision_rows_list.append(data)
precision_df = pd.DataFrame(precision_rows_list)
precision_html_table = precision_df.to_html(index=False)

# Same for recall json
recall_rows_list = []
with open(recall_json, 'r') as json_file:
    data=json.load(json_file)
    recall_rows_list.append(data)
recall_df = pd.DataFrame(recall_rows_list)
recall_html_table = recall_df.to_html(index=False)



with open(template, 'r') as template_file:
    contents = template_file.read()
    template_soup = BeautifulSoup(contents, features="html.parser")

h2_list = template_soup.find_all('h2')

h2_list[0].insert_after(recall_html_table)
h2_list[1].insert_after(precision_html_table)

with open('spot_detection_qc_report.html', 'w') as result_file:
    result_file.write(str( template_soup ))

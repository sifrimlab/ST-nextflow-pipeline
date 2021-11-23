import json
from bs4 import BeautifulSoup
import pandas as pd
import sys

# Argparsing
argument_index = 1
template = sys.argv[argument_index]
argument_index +=1

recall_json = sys.argv[argument_index]
argument_index +=1

recall_plot = sys.argv[argument_index]
argument_index +=1

precision_jsons_list = [sys.argv[i] for i in range(argument_index, len(sys.argv))]

precision_rows_list = []
# convert jsons back to dicts for html conversion
for json_path in precision_jsons_list:
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
        precision_rows_list.append(data)
precision_df = pd.DataFrame(precision_rows_list)
precision_df = precision_df.sort_values(by='Round #')
precision_html_table = precision_df.to_html(index=False)

# Same for recall json
recall_rows_list = []
with open(recall_json, 'r') as json_file:
    data=json.load(json_file)
    recall_rows_list.append(data)
recall_df = pd.DataFrame(recall_rows_list)
recall_html_table = recall_df.to_html(index=False)


# Create html

with open(template, 'r') as template_file:
    contents = template_file.read()
    template_soup = BeautifulSoup(contents, features="html.parser")

p_list = template_soup.find_all('p')
p_index = 0

# Read recall table tag
recall_soup = BeautifulSoup(recall_html_table, features="html.parser")
table_tag = recall_soup.find('table')
p_list[p_index].insert_after(table_tag)
p_index+=1

image_tag = template_soup.new_tag('img')
image_tag['src']= f"./recall/{recall_plot}"
image_tag['width']= 700
image_tag['height']= 500
p_list[p_index].insert_after(image_tag)
p_index+=1



precision_soup = BeautifulSoup(precision_html_table, features="html.parser")
table_tag = precision_soup.find('table')
p_list[p_index].insert_after(table_tag)
p_index+=1

with open('spot_detection_qc_report.html', 'w') as result_file:
    result_file.write(str( template_soup ))

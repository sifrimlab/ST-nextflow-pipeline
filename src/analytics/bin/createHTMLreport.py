from bs4 import BeautifulSoup
import pandas as pd
import sys

template = sys.argv[1]
image_list = [sys.argv[i] for i in range(2,4) ]
table_list = [sys.argv[i] for i in range(4, len(sys.argv))]
with open(template, 'r') as template_file:
    contents = template_file.read()
    template_soup = BeautifulSoup(contents, features="html.parser")

h2_list = template_soup.find_all('h2')
h2_index = 0
for element in table_list:
    with open(element, 'r') as html_file:
        contents = html_file.read()
        html_soup = BeautifulSoup(contents, features='html.parser')
        table_tag = html_soup.find('table')
        h2_list[h2_index].insert_after(table_tag)
        h2_index+=1

for element in image_list:
        image_tag = template_soup.new_tag('img')
        image_tag['src']= element
        image_tag['width']= 500
        image_tag['height']= 500
        h2_list[h2_index].insert_after(image_tag)
        h2_index+=1

with open('decoding_report.html', 'w') as result_file:
    result_file.write(str( template_soup ))

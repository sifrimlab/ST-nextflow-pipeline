from bs4 import BeautifulSoup
import pandas as pd
import sys

template = sys.argv[1]
tag_list = [sys.argv[i] for i in range (2,len(sys.argv))]
# image_list = [sys.argv[i] for i in range(2,4) ]
# table_list = [sys.argv[i] for i in range(4, len(sys.argv))]

with open(template, 'r') as template_file:
    contents = template_file.read()
    template_soup = BeautifulSoup(contents, features="html.parser")
    

h2_list = template_soup.find_all('h2')

for i in range(0,6):
    with open(tag_list[i], 'r') as html_file:
        contents = html_file.read()
        html_soup = BeautifulSoup(contents, features='html.parser')
        table_tag = html_soup.find('table')
        h2_list[0].insert_after(table_tag)
for i in range(6,8):
        image_tag = template_soup.new_tag('img')
        image_tag['src']= tag_list[i]
        image_tag['width']= 500
        image_tag['height']= 500
        h2_list[i].insert_after(image_tag)
with open('decoding_report.html', 'w') as result_file:
    result_file.write(str( template_soup ))

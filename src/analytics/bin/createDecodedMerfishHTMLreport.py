import sys
from bs4 import BeautifulSoup

template = sys.argv[1]


table_list = [sys.argv[i] for i in range(2,5) ]
image_list = [sys.argv[i] for i in range(5, len(sys.argv))]

with open(template, 'r') as template_file:
    contents = template_file.read()
    template_soup = BeautifulSoup(contents, features="html.parser")

p_list = template_soup.find_all('p')
p_index = 0

for element in table_list:
    with open(element, 'r') as html_file:
        contents = html_file.read()
        html_soup = BeautifulSoup(contents, features='html.parser')
        table_tag = html_soup.find('table')
        p_list[p_index].insert_after(table_tag)
        p_index+=1



for element in image_list:
        image_tag = template_soup.new_tag('img')
        image_tag['src']= f"assets/{element}"
        image_tag['width']= 1200
        image_tag['height']= 800
        p_list[p_index].insert_after(image_tag)
        p_index+=1

with open('decoding_report.html', 'w') as result_file:
    result_file.write(str( template_soup ))

import sys
from bs4 import BeautifulSoup

template = sys.argv[1]

table_list = [sys.argv[i] for i in range(2,7) ]
image_list = [sys.argv[i] for i in range(7, 8)]
tile_list = [sys.argv[i] for i in range(8, 10)] # first = table, second = image
decoding_potential_plot = sys.argv[10]
decoding_intensity_QC_plot = sys.argv[11]

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

with open(tile_list[0], 'r') as html_file:
    contents = html_file.read()
    html_soup = BeautifulSoup(contents, features='html.parser')
    table_tag = html_soup.find('table')
    h2_list[h2_index].insert_after(table_tag)
    h2_index+=1

# Tile image
image_tag = template_soup.new_tag('img')
image_tag['src']= tile_list[1]
image_tag['width']= 500
image_tag['height']= 500
h2_list[h2_index].insert_after(image_tag)
h2_index+=1

# Decoding potential image
image_tag = template_soup.new_tag('img')
image_tag['src']= decoding_potential_plot
image_tag['width']= 500
image_tag['height']= 500
h2_list[h2_index].insert_after(image_tag)
h2_index+=1

# Decoding intensity QC
image_tag = template_soup.new_tag('img')
image_tag['src']= decoding_intensity_QC_plot
image_tag['width']= 800
image_tag['height']= 500
h2_list[h2_index].insert_after(image_tag)
h2_index+=1


with open('decoding_report.html', 'w') as result_file:
    result_file.write(str( template_soup ))

import sys
from bs4 import BeautifulSoup

template = sys.argv[1]

table_list = [sys.argv[i] for i in range(2,7) ]
image_list = [sys.argv[i] for i in range(7, 9)]
tile_list = [sys.argv[i] for i in range(9, 11)] # first = table, second = image
decoding_potential_plot = sys.argv[11]
decoding_potential_plot_per_tile = [sys.argv[i] for i in range(12, len(sys.argv))]

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

def addListOfImages(template_soup, image_list, h2_title_index):
    # Plot first image 
    image_tag = template_soup.new_tag('img')
    image_tag['src']= image_list[0]
    image_tag['width']= 500
    image_tag['height']= 500
    h2_list[h2_title_index].insert_after(image_tag)
    # then plot the other images right after the previous one
    for i,image in enumerate(image_list):
        if i==0:
            previous_image = image_tag
            continue
        else:
            image_tag = template_soup.new_tag('img')
            image_tag['src']= image
            image_tag['width']= 500
            image_tag['height']= 500
            previous_image.insert_after(image_tag)
            previous_image=image_tag

# Plot individual tile decoding potential plot
addListOfImages(template_soup, decoding_potential_plot_per_tile, h2_index)
h2_index+=1

with open('decoding_report.html', 'w') as result_file:
    result_file.write(str( template_soup ))

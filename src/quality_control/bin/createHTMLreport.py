from bs4 import BeautifulSoup
import pandas as pd
import sys

template = sys.argv[1]
intensities = sys.argv[2]
image_list = [sys.argv[i] for i in range(3, len(sys.argv))]
image_list.sort()

with open(template, 'r') as template_file:
    contents = template_file.read()
    template_soup = BeautifulSoup(contents, features="html.parser")
with open(intensities, "r") as intensity_file:
    contents = intensity_file.read()
    intensity_soup = BeautifulSoup(contents, features="html.parser")
    table_tag = intensity_soup.find('table')

h2_list = template_soup.find_all('h2')
#for h2 in h2_list:
#    names = h2.contents[0]
#print(names[0])

h2_list[0].insert_after(table_tag)

# Plot first image 
image_tag = template_soup.new_tag('img')
image_tag['src']= image_list[0]
image_tag['width']= 500
image_tag['height']= 500
h2_list[1].insert_after(image_tag)

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
with open('quality_control_report.html', 'w') as result_file:
    result_file.write(str( template_soup ))

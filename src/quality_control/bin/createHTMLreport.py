from bs4 import BeautifulSoup
import pandas as pd
import sys

argument_index = 1
nr_rounds = int(sys.argv[argument_index])
argument_index +=1
nr_channels = int(sys.argv[argument_index])
argument_index +=1

template = sys.argv[argument_index]
argument_index +=1
intensities = sys.argv[argument_index]
argument_index +=1
combined_round_histograms = [sys.argv[i] for i in range(argument_index,argument_index+nr_rounds)]
argument_index += nr_rounds
combined_channel_histograms = [sys.argv[i] for i in range(argument_index, argument_index+nr_channels)]
argument_index += nr_channels

intensity_histograms_per_image=[sys.argv[i] for i in range(argument_index, len(sys.argv))] 

combined_round_histograms.sort()
combined_channel_histograms.sort()
intensity_histograms_per_image.sort()

with open(template, 'r') as template_file:
    contents = template_file.read()
    template_soup = BeautifulSoup(contents, features="html.parser")
with open(intensities, "r") as intensity_file:
    contents = intensity_file.read()
    intensity_soup = BeautifulSoup(contents, features="html.parser")
    table_tag = intensity_soup.find('table')

# add Intensity Statistics Per Image
h2_list = template_soup.find_all('h2')
h2_list[0].insert_after(table_tag)

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

# add Combined Round Histograms
addListOfImages(template_soup, combined_round_histograms, 1)

# add Combined Channel Histograms
addListOfImages(template_soup, combined_channel_histograms, 2)

# add all plots
addListOfImages(template_soup, intensity_histograms_per_image, 3)

with open('quality_control_report.html', 'w') as result_file:
    result_file.write(str( template_soup ))

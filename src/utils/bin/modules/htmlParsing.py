from bs4 import BeautifulSoup
import pandas as pd
import sys

intensities = "/home/david/Documents/communISS/results/quality_control/combined_intensity_analytics.html"

with open(intensities, "r") as html_file:
    contents = html_file.read()
    soup = BeautifulSoup(contents, features="html.parser")
    print(soup)
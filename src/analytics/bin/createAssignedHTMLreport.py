import sys
from bs4 import BeautifulSoup

template = sys.argv[1]

table_list = [sys.argv[i] for i in range(2,len(sys.argv))]

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

with open('assignment_report.html', 'w') as result_file:
    result_file.write(str( template_soup ))

import requests
import os
import time
from bs4 import BeautifulSoup
from os.path import basename


# The presentation of the program
print("\nWelcome to the Python program 'Vasca_Scraper'.\
      \n\nThe program allows you to scrape the 'cde.ca.gov' webpage")

# The directory you want to work on
directory = input("\nPlease write the directory you want to work on,\
 starting from /home (included),\nseparating each directory with /\n\
(the notation may be different if you are using Windows or MacOS).\n\n\
No inverted commas are required.\n\
Press 'Enter' if you want to use the current directory.\n")
time.sleep(1)

# The name of the folder containing the files
name = input("\nPlease write the name of the directory \
containing all .xls files.\n\
Press 'Enter' if you accept the default option:\n\
'Vasca_Scraper_FILES'.\n")

if name == '':
    name = 'Vasca_Scraper_FILES'

print("The program has started working. Please wait ...")

# The name of the website
url = "http://www.cde.ca.gov/ds/sp/ai/"
r = requests.get(url)
page = r.text

# Move to the chosen directory (if allowed)
try:
    os.chdir(directory)
except:
    directory = os.getcwd()

# Create the folder and start working
os.makedirs(name)
os.chdir(directory + "/" + name)

soup = BeautifulSoup(page, 'lxml')
link = soup.findAll('a')

sat = []
act = []
ap = []
dates = ['99'] + ['0'+str(i) for i in range(10)] + [str(i) for i in range(10,17)]

######################
# working on SAT files

for i in range(len(link)):
    if len(link[i].contents) > 0 and 'SAT' in link[i].contents[0]:
        sat += [link[i].get('href')]

for j in sat:
    for g in dates:
        nm = "sat" + g + ".xls"
        if nm in j:
            if "http" not in j:
                j = "https://www.cde.ca.gov/ds/sp/ai/" + j
            resul = requests.get(j)
            file = open(basename(j), 'wb')
            file.write(resul.content)
            file.close()

print("SAT files have been downloaded into " + name + " folder.")

######################
# working on ACT files

for i in range(len(link)):
    if len(link[i].contents) > 0 and 'ACT' in link[i].contents[0]:
        act += [link[i].get('href')]

for j in act:
    for g in dates:
        nm = "act" + g + ".xls"
        if nm in j:
            if "http" not in j:
                j = "https://www.cde.ca.gov/ds/sp/ai/" + j
            resul = requests.get(j)
            file = open(basename(j), 'wb')
            file.write(resul.content)
            file.close()

print("ACT files have been downloaded into " + name + " folder.")

######################
# working on AP files

for i in range(len(link)):
    if len(link[i].contents) > 0 and 'AP' in link[i].contents[0]:
        ap += [link[i].get('href')]

for j in ap:
    for g in dates:
        nm = "ap" + g + ".xls"
        if nm in j:
            if "http" not in j:
                j = "https://www.cde.ca.gov/ds/sp/ai/" + j
            resul = requests.get(j)
            file = open(basename(j), 'wb')
            file.write(resul.content)
            file.close()

print("AP files have been downloaded into " + name + " folder.")

print("Vasca_Scraper has done his job. Thank you for choosing me.")

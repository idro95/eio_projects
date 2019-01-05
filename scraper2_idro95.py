import requests
import platform
import os
import time
from bs4 import BeautifulSoup
from os.path import basename
import tabula
import pandas
import csv
import re


# The presentation of the program
print("\nWelcome to the Python program 'Vasca_Scraper_II'.\
      \n\nThe program allows you to scrape the 'codot.gov' webpage\n \
      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
time.sleep(1)

# The directory you want to work on
print('You are currently working on the following directory: \n' + os.getcwd())
directory = input("\nPlease write the complete path of the directory you want to work on.\n\
No inverted commas are required.\n\
Press 'Enter' if you want to use the current directory.\n")
time.sleep(1)

# The name of the folder containing the files
name = input("\nPlease write a name for the folder \
that will contain all .pdf and .csv files.\n\
Press 'Enter' if you accept the default option:\n\
'ProblemSet3_FILES'.\n")

if name == '':
    name = 'ProblemSet3_FILES'

# Move to the chosen directory (if possible)
try:
    os.chdir(directory)
except:
    if directory != '':
        print('Sorry, the directory you have chosen is not allowed.\n \
The program will use the current directory.')
    directory = os.getcwd()

# /&£/DONE/&£/ Uncomment the lines following the sign
# '/&£/DONE/&£/' if you already have downloaded all .pdf files
# By doing so, the code will directly start from the "pdf-files-scraping"

#step = input('\nPlease type "d" if you want to perform only the .csv file part. Otherwise press anything else.\n')

# Create the folder and start working

# /&£/DONE/&£/
# the following 6 lines of code must be used as an alternative to the subsequent 5 (the other try)
#try:
#    os.chdir(directory)
#    if step != 'd':
#        os.makedirs(name)
#except FileExistsError:
#    pass

try:
    os.chdir(directory)
    os.makedirs(name)
except FileExistsError:
    pass

# We move to the folder chosen by the user
if platform.system() == 'Windows':
    os.chdir(directory + "\\" + name)
else:
    os.chdir(directory + "/" + name)

# This part downloads the files from the website

# /&£/DONE/&£/ If you uncomment the following line,
# please make sure you tab all lines up to "/&£/DONE/&£/END"
#if step != 'd':

print("The program has started working. Please wait ...")

# The name of the website
url = "https://www.codot.gov/business/bidding/bid-tab-archives" # web page for 2018
r = requests.get(url)
page = r.text

soup = BeautifulSoup(page, 'lxml')
link = soup.find('div',{'id' : 'content-core'}).find("table")

# Create the list for all hrefs
hrefs = []

# Check the content and plug the hrefs in the list
for p in link.findAll('a', href = True):
    if 'Bid Tab' in p.contents[0]:
        hrefs += [p['href']]

# Download and save all .pdf files in the decided folder
counter = 0
for j in hrefs:
    pdf = requests.get(j)
    namepdf = j.split("/")[-1] + '.pdf'
    try:
        file = open(namepdf, 'wb')
        file.write(pdf.content)
        file.close()
        counter += 1
    except FileNotFoundError:
        pass

# Optional: it tells you how many files have been downloaded.
# They should be 104 (however, one of them is damaged)
print("\nThe folder " + name + " contains " + str(counter) + " files.\n")

# /&£/DONE/&£/END

# The following code extracts the data of interest from pdf files
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
name_csv = input('\nPlease enter a name for the .csv final file.\n\
By pressing "Enter" you accept the default option: "data_bids.csv".\n')
if name_csv == '':
    name_csv = 'data_bids.csv'
else:
    if name_csv[-4:] != '.csv':
        name_csv = name_csv + '.csv'

with open(name_csv, 'a') as csv_file: # create a .csv file to contain the dataset
    dataset = csv.writer(csv_file)
    dataset.writerow(['Auction_code','Number_of_participants','Winning_bid'])
    # we are interested only in three data: an identifier of the auction,
    # the number of bidders and the winning bid
    print('The number of file I will use for the .csv is ' + str((len(os.listdir()))-1))
    fail = [] # this list will contain the names of the files we can't open
    for name_file in os.listdir():
        try:
            # we only take the table at the second page of each file
            file2 = tabula.read_pdf(name_file, pages = '2', multiple_tables = True)
            # we find the univocal identification code of the auction
            auc_code = name_file.split(".")[0]
            # we clean the table of headers
            file2_clean = file2[0][pandas.notnull(file2[0][0])]
            file2_clean = file2_clean.loc[2:] # we leave only the numerical values
            # we find the number of participants in the bid
            num_bid = max(list(file2_clean[0]))
            # we find the winning bid and eliminate the '$' or '%' from it
            winner = file2_clean[4][file2_clean[0] == '1'].item().replace('$','')
            if '%' in winner: # we change winner for particular files
                winner = file2_clean[3][file2_clean[0] == '1'].item().replace('$','')
            # the part added to the csv file is the following row
            c = winner
            c = c.replace(',','')
            c = float(c)
            add = [auc_code, num_bid, c]
            dataset.writerow(add) # we add the row
        except: # if the file format is different, we deal with it later
            if name_file not in [name_csv, 'mtce-r100-312-22471.pdf']:
                fail += [name_file]
            continue

with open(name_csv, 'a') as csv_file: # create a .csv file to contain the dataset
    dataset = csv.writer(csv_file)
    # In that final part of the code we deal with the files we didn't manage to open before
    # I thank Silvio Busonero and Carolina Maffini for helping me with this final part
    for i in fail:
        name_file = i
        # we find the univocal identification code of the auction
        auc_code = name_file.split(".")[0]
        try:
            file2 = tabula.read_pdf(name_file, pages = '1', multiple_tables = False, guess = False)
            # we take the bid
            winner = file2.loc[4][4].replace('$','')
            # we find the number of participants in the bid
            num_bid = file2.loc[4][2]
            # the part added to the csv file is the following row
            winner = winner.replace(',','')
            c = float(winner)
            add = [auc_code, num_bid, c]
            dataset.writerow(add) # we add the row
        except:
            continue

print("\nVasca_Scraper_II has done his job. Thank you for choosing me.")

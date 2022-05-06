import mysql.connector
from datetime import datetime
import time
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import csv
import requests 
import json
import math


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

#setup senator scraping
url = "https://www.senate.gov/senators/index.htm"
req = Request(url,headers=headers)
senate_page = urlopen(req)
soup = BeautifulSoup(senate_page)

#scrape senator table
data_senators = soup.find("table", {"id": "listOfSenators"}).find('tbody').findAll('tr')

#[name, url, state, party, class]
sen_metadata = []
for row in data_senators:
    children = row.findChildren()[1:]
    metadata = [children[0].text, children[0].get('href'), children[1].text, children[2].text, children[4].text]
    sen_metadata.append(metadata)

#setup senator scraping
url = "https://www.senate.gov/senators/NewSenators.htm"
req = Request(url,headers=headers)
swearing_page = urlopen(req)
soup = BeautifulSoup(swearing_page)

#scrape date of swearing table
data_senators = soup.find("table").find('tbody').findAll('tr')[1:]

#loop through and obtain list of dates for each senator
sen_terms = []
for row in data_senators:
    children = row.findChildren()
    date_swearing = children[5] if len(children) >= 8 else children[-1]
    if date_swearing.name == 'td':
        name = (children[0].text).split(' ')[-1]
        datetime_object = datetime.strptime(date_swearing.text, '%B %d, %Y')
        diff = abs((datetime_object - datetime.today()).days)
        term = math.floor(diff/(365*6)) + 1
        term = term if term < 4 else 3
        metadata = (name, term)
        sen_terms.append(metadata)

cnx = mysql.connector.connect(user='toutvisadmin', password='aa5HZeJ2tahR5Gyz',
                              host='eltanin',
                              database='TextOutlierVis')

cursor = cnx.cursor()

for sen in sen_metadata:
    last_name = sen[0].split(',')[0]
    sen_class = sen[-1]
    add_class = (f"UPDATE senators SET sen_class = %s WHERE sen_last_name = '{last_name}'")
    cursor.execute(add_class, (sen_class,))

for last_name, term in sen_terms:
    add_term = (f"UPDATE senators SET sen_term = %s WHERE sen_last_name = '{last_name}'")
    cursor.execute(add_term, (term,))

cnx.commit()
cnx.close()
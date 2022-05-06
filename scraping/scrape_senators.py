import numpy as np
from pathlib import Path  
import pandas as pd
import os, random
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import csv
import requests
from crochet import setup, wait_for
from time import strptime
import datetime



#for inserting into database
import mysql.connector
import datetime
import time
from mysql.connector.errors import Error

cnx = mysql.connector.connect(user='toutvisadmin', password='aa5HZeJ2tahR5Gyz',
                              host='eltanin',
                              database='TextOutlierVis')

cursor = cnx.cursor()
#for timestamp insert
ts = time.time()
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

#insert parties
insert_parties = False
if insert_parties:
    add_party = ("INSERT INTO parties"
                "(party_id, name, color) "
                "VALUES (%s, %s, %s)")
    add_party_data = [(0, 'democratic', 'red'), (1, 'republican', 'blue'), (2, 'independent', 'green')]
    cursor.executemany(add_party, parties)

insert_states = False
if insert_states:
    add_state = ("INSERT INTO states"
               "(state_name, state_gdp, state_population) "
               "VALUES (%s, %s, %s)")

    add_state_data = ["Alaska", "Alabama", "Arkansas", "Arizona", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]

    for state in states:
        cursor.execute(add_state, (state, 0, 0))




#scrape senator webpages
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
req = Request("https://www.congress.gov/members?pageSize=250&q=%7B%22congress%22%3A%22117%22%2C%22chamber%22%3A%22Senate%22%7D",headers=headers)
senate_page = urlopen(req)

senator_websites = []
temp = []

soup = BeautifulSoup(senate_page, features='lxml')
data_senators = soup.findAll("span",{'class':"result-heading"})
for i in data_senators:
    children = i.findChildren('a', recursive=False)
    temp.append(children[0].text)
    website = "http://congress.gov" + children[0].get('href')
    senator_websites.append(website)




#scraping
#scrape senator parties and states
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
req = Request("https://www.congress.gov/members?pageSize=250&q=%7B%22congress%22%3A%22117%22%2C%22chamber%22%3A%22Senate%22%7D",headers=headers)
senate_page = urlopen(req)

states = []
parties = []

soup = BeautifulSoup(senate_page, features='lxml')
data_results = soup.findAll("span",{'class':"result-item"})
i = 0
is_state = True
clean = re.compile('<.*?>')

for result in data_results:
    if i % 2 == 0:
        span = result.find_next('span')
        if span.string != None:
            if is_state:
                states.append(re.sub(clean, '', span.string))
                is_state = False
            else:
                parties.append(re.sub(clean, '', span.string))
                is_state = True
    i+=1


senator_names = []
senator_states = []

#scrape senator_names
for i in range(len(temp)):
    t = str(temp[i])
    regEx = re.compile('([A-Z][a-z]*),.*')
    if (regEx.search(t)):
        res = regEx.search(t)
        senator_names.append(res.group(0))
        regEx1 = re.compile('[A-Z][A-Z]')
        if (regEx1.search(t)):
            res1 = regEx1.search(t)

#remove duplicates
senator_names = list(set(senator_names))
senator_websites = list(set(senator_websites))

#remove commas from senator_names
for i in range(len(senator_names)):
    tmp = str(senator_names[i])
    sen_no_comma = tmp.replace(',','')
    sen_name = sen_no_comma.split()
    senator_names[i] = sen_name[0] + " " + sen_name[1]

i = 0
senator_parties=[]
for sen in senator_names:
    party = parties[i]
    senator_parties.append((sen, party))
    i+=1

for i in range(len(senator_websites)):
    name = senator_names[i]
    web = senator_websites[i]
    senator_websites[i] = (name, web)

us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}

abbrev_to_full_month = {'Jan': 'January', 'Ja': 'January', 'Fe': 'February', 'Feb': 'February', 'Ma': 'March', 'Marc': 'March', 'Apr': 'April', 'Ap': 'April', 
'Apri': 'April', 'Ma': 'May', 'May': 'May', 'Jun': 'June', 'Ju': 'July', 'Jul': 'July', 'Aug': 'August', 'Sep': 'September', 'Sept': 'September', 'Oc': 'October', 'Oct': 'October', 'Nov': 'November', 'De': 'December', 'Dec': 'December'}

for s in states:
    senator_states.append(us_state_to_abbrev[s])


insert_senators = False
if insert_senators:
    add_senator = ("INSERT INTO senators"
               "(sen_first_name, sen_last_name, party_id, state_id, sen_homepage) "
               "VALUES (%s, %s, %s, %s, %s)")
    for i in range(len(senator_names)):
        party_id = f"select party_id from parties where party_name='{parties[i]}'"
        state_id = f"select state_id from states where state_name='{states[i]}'"
        cursor.execute(party_id)
        party_id = cursor.fetchall()[0][0]
        cursor.execute(state_id)
        state_id = cursor.fetchall()[0][0]
        add_senator_data = (senator_names[i].split()[1], senator_names[i].split()[0], party_id, state_id, senator_websites[i][1])
        cursor.execute(add_senator, add_senator_data)
    cnx.commit()
    cursor.close()

senator_links = []
senator_dates = []
senator_titles = []

for i in range(len(senator_names)):
    search = True
    current_state = senator_states[i]
    current_name = senator_names[i]
    links = []
    page_numb = 1
    doc_count = 0
    sen_website = False
    titles = []
    dates = []
   
    url = "https://projects.propublica.org/represent/statements?by_state="+str(current_state)+"&page="
    print("Fetching: ", current_name)
   
#     if search finds no documents, go to website of senator and scrape from there
    while search:
        print("Page: ", page_numb)
        link = url + str(page_numb)
        r = requests.get(link)
        soup = BeautifulSoup(r.content, features='lxml')
        table = soup.find("table")
        rows = table.findAll('tr')
        for row in rows:
            temp = row.find_all("a")
            name = temp[0].text
            names = name.split()
            name = names[1] + " " + names[0]
            cols = row.findAll("td")
            if name == current_name and doc_count < 50:
                col_data = []
                for col in cols:
                    col_data.append(col.findChildren(text=True)[0])
                col_date = col_data[0].split(' ')
                date_str = '2022-' + abbrev_to_full_month[col_date[0][:-1]] + '-' + col_date[1].replace(',', '')
                datetime_object = datetime.datetime.strptime(date_str, '%Y-%B-%d')
                dates.append(datetime_object)
                titles.append(col_data[4])
                links.append(temp[1].get('href'))
                doc_count += 1
                
        if doc_count >= 50:
            search = False
        elif page_numb > 10:
            sen_website = True
            search = False
        page_numb += 1
    
    senator_links.append(links)
    senator_dates.append(dates)
    senator_titles.append(titles)

# This one fetches text data from a multiple page
# by keeping unwanted tags in a seperate list
# by using regex to remove tags

for i in range(len(senator_names)): # change if require less number of links
    links_list = senator_links[i]
    dates_list = senator_dates[i]
    titles_list = senator_titles[i]

    if links_list == []:
        continue
    name = str(senator_names[i])
    for i in range(len(links_list)):
        req = Request(links_list[i],headers=headers)
        try:
            html_page = urlopen(req)
            print("Success: " + name)
        except:
            print("Failed Connection: " + links_list[i])
            continue

        p = re.compile('<.*?>')  
        soup = BeautifulSoup(html_page, "lxml")
        Printxt = ""
        if soup is not None:
            for para in soup.findAll('p'):
                if (p.search(str(para))):
                    Printxt += para.get_text()
            if(len(Printxt) > 50):
                #insert into database
                add_senator = ("INSERT INTO docs"
                    "(doc_text, doc_link, sen_id, doc_title, doc_date) "
                    "VALUES (%s, %s, %s, %s, %s)")
                cursor.execute(f"select sen_id from senators where sen_last_name='{name.split()[0]}'")
                sen_id = None
                sen_id = cursor.fetchall()[0][0]
                if sen_id is not None:
                    add_senator_data = (Printxt, links_list[i], sen_id, str(titles_list[i]), str(dates_list[i]))
                else:
                    add_senator_data = (Printxt, links_list[i], 0, str(titles_list[i]), str(dates_list[i]))
                
                try:
                    cursor.execute(add_senator, add_senator_data)
                except:
                    print(str(Error()))
cnx.commit()
cursor.close()
        
# df = pd.DataFrame(list(zip(Name_Data,Text_Data,Link_Data)), columns =['name','description', 'url'])
# print(df.head())
# def clean_text(s):
#     s = s.lower()
#     s = utils.to_unicode(s)
#     for f in filters:
#         s = f(s)
#     return s
# # df['description'] = df['description'].map(lambda x: clean_text(x))
# filepath = Path('./out.csv')  
# filepath.parent.mkdir(parents=True, exist_ok=True)  
# df.to_csv(filepath)  
# compression_opts = dict(method='zip', archive_name="test.csv")
# df.to_csv('test.zip', index=False, compression=compression_opts)

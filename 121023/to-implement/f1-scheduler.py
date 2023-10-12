#Run only once. To scrape the schedule and export into JSON
import requests
from bs4 import BeautifulSoup
import json
import os

url = 'https://www.formula1.com/en/latest/article.formula-1-announces-calendar-for-2024.XL3c5Cxi0ZOQzPrUu5izL.html'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

tables = soup.find_all('table')
db = {
    "Date": "",
    "GrandPrix": "",
    "Venue":""

}
db_list = []
for table in tables:
    rows = table.find_all('tr')
    for row in rows:
        cells = row.find_all(['th', 'td'])
        for cell in cells:
            a = cell.text
            if "\xa0" in a:
                a = a.replace('\xa0', ' ')
            db_list.append(a)

db_list = db_list[3:]
big_date = []
big_gp = []
big_venue = []

i=0

while i<len(db_list):
    try:
        big_date.append(db_list[i])
        big_gp.append(db_list[i+1])
        big_venue.append(db_list[i+2])
        i+=3
    except Exception:
        break

db["Date"] = big_date
db["GrandPrix"] = big_gp
db["Venue"] = big_venue
with open('f1-schedule.json', 'w') as json_file:
    json.dump(db, json_file)
    
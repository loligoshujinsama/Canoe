from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time as t
import requests
from datetime import *
import pandas as pda
import openpyxl
from selenium.webdriver.support.select import Select

url = f"https://www.expedia.com.sg/Hotel-Search?adults=1&d1=2023-10-10&d2=2023-10-12&destination=Bangkok%20%28and%20vicinity%29%2C%20Bangkok%20Province%2C%20Thailand&endDate=2023-10-13&regionId=178236&rooms=1&semdtl=&sort=RECOMMENDED&startDate=2023-10-12&theme=&useRewards=false&userIntent="
a = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=a)

driver.get(url)
t.sleep(5)

name_list = []
price_list = []
rating_list = []

hotel_elements = driver.find_elements(By.XPATH, "//div[@class='uitk-layout-flex uitk-layout-flex-block-size-full-size uitk-layout-flex-flex-direction-column uitk-layout-flex-justify-content-space-between']")
for hotel_element in hotel_elements:
    hotel_name = hotel_element.find_element(By.XPATH, ".//h3[@class='uitk-heading uitk-heading-5 overflow-wrap uitk-layout-grid-item uitk-layout-grid-item-has-row-start']")
    hotel_price = hotel_element.find_element(By.XPATH, ".//div[@class='uitk-text uitk-type-500 uitk-type-medium uitk-text-emphasis-theme']")
    hotel_rating = hotel_element.find_elements(By.XPATH, ".//span[@class='uitk-badge-base-text']")
    if hotel_rating:
        rating = hotel_rating[0].text
    else:
        rating = 'No ratings found'
    name_list.append(hotel_name.text)
    price_list.append(hotel_price.text)
    rating_list.append(rating)

db = {
    "hotel_name": "",
    "hotel_price": "",
    "hotel_rating": ""
}

def excel(a):
    df = pda.DataFrame(a)
    df.to_excel("H:/hotel.xlsx")

db["hotel_name"] = name_list
db["hotel_price"] = price_list
db["hotel_rating"] = rating_list
print(db)
excel(db)

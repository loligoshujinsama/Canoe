from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import requests
import sys

'''
departure="SIN"
destination="BKK"
dep_date="2023-11-11"
arrival_date="2023-11-11"
'''


departure=input("Departure location (e.g SIN/BKK): ")
destination= input("Destination location (e.g SIN/BKK): ")
dep_date=input("Date of departure? (e.g. 2023-11-11): ")
arrival_date=input("Date of return? (e.g. 2023-11-11): ")

db={}

URL = f'https://www.kayak.com/flights/{departure}-{destination}/{dep_date}/{arrival_date}?sort=bestflight_a'
print(URL)

def provider():
    array_provider=[]
    for element in driver.find_elements(By.CLASS_NAME, 'M_JD-provider-name'):
        array_provider.append(element.text)
    return array_provider

def price():
    array_price=[]
    for element in driver.find_elements(By.CLASS_NAME, 'f8F1-price-text'):
        array_price.append(element.text)
    return array_price

def output(a,b):
    for i in range(len(a)):
        print("Provider: "+str(a[i])+" Price: "+str(b[i]))

if __name__ == '__main__':
    try:
        a = webdriver.ChromeOptions()
        #a.add_argument('--headless')
        driver = webdriver.Chrome(options=a)
        driver.get(URL)
        time.sleep(10)
        a1 = provider()
        time.sleep(5)
        a2 = price()
        time.sleep(5)

        output(a1,a2)
    except Exception as e:
        print(e.args)
        webdriver.close()

    #Put this in a dictionary, so easier to parses data.
    #Additionally, can also make several keys to invoke the data based on key

    

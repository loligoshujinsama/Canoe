from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import requests
import sys
import pandas as pda
import pprint
import openpyxl
import airportsdata

departure="SIN"
destination="BKK"
dep_date="2023-11-11"
return_date="2023-11-11"

db={
    "Provider":"",
    "Price":"",
    "Departure-time":"",
    "Departure-airline":"",
    "Return-time":"",
    "Return-airline":""
}

URL = f'https://www.kayak.com/flights/{departure}-{destination}/{dep_date}/{return_date}?sort=bestflight_a'
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

def flight_time_and_airline():
    counter=[]
    for element in driver.find_elements(By.CLASS_NAME, 'VY2U'):
        counter.append(element.text)
        flight_time_departure=[]
        flight_time_return=[]
        for i in range(len(counter)):
            if i % 2 ==0:
                flight_time_departure.append(counter[i])
            else:
                flight_time_return.append(counter[i])
                
    
    #Extract flight time and airline
    rt=[]
    ra=[]
    dt=[]
    da=[]
    for i in range(len(flight_time_return)):
        temp=[]
        temp=flight_time_return[i].split('\n')
        rt.append(temp[0])
        ra.append(temp[1])
    
    for i in range(len(flight_time_departure)):
        temp=[]
        temp=flight_time_departure[i].split('\n')
        dt.append(temp[0])
        da.append(temp[1])
    
    db["Return-time"]=rt
    db["Return-airline"]=ra
    db["Departure-time"]=dt
    db["Departure-airline"]=da
    return None

def debugger(a,b):
    for i in range(len(a)):
        print("Provider: "+str(a[i])+" Price: "+str(b[i]))

def excel(a):
    df = pda.DataFrame(a)

    #Debugging
    #print(df)
    df = df.sort_values(by=["Price"])
    df.to_excel("H:/output.xlsx")
    

    #Note to user: xlsx must not be opened, or there will be permission issues

if __name__ == '__main__':
    try:
        a = webdriver.ChromeOptions()
        #a.add_argument('--headless')
        driver = webdriver.Chrome(options=a)
        driver.get(URL)
        time.sleep(10)
        a1 = provider()
        a2 = price()
        flight_time_and_airline()
        db["Provider"] = a1
        db["Price"] = a2
        excel(db)
        #Nicely print dictionary
        #pprint.pprint(db)

    except Exception as e:
        driver.quit()
        print(e.args)
    

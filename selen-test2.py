from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time as t
import requests
from datetime import *
import sys
import pandas as pda
import openpyxl
from selenium.webdriver.support.select import Select
#import airportsdata


departure = sys.argv[1]
destination = sys.argv[2]
dep_date = sys.argv[3]

db={
    "Provider":"",
    "Price":"",
    "Departure-time":"",
    "Departure-airline":""
}

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
        for i in range(len(counter)):
            flight_time_departure.append(counter[i])
                

    #Extract flight time and airline
    dt=[]
    da=[]
    
    for i in range(len(flight_time_departure)):
        temp=[]
        temp=flight_time_departure[i].split('\n')
        dt.append(temp[0])
        da.append(temp[1])
    
    #db["Departure-time"]=dt
    #db["Departure-airline"]=da

    return dt, da

def dateAppender(dep_date):
    format = '%Y-%m-%d'
    dep_date = datetime.strptime(dep_date,format)

    next7=[]
    for i in range(28):
        a = str(dep_date)
        a=a.split(" ")
        next7.append(a[0])
        dep_date = dep_date + timedelta(days=1)
    return next7

def excel(a):
    df = pda.DataFrame(a)

    #Debugging
    #print(df)
    df = df.sort_values(by=["Price"])
    df.to_excel("H:/output.xlsx")
    

if __name__ == '__main__':
    try:
        a = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=a)
        big_prov = []
        big_price = []
        big_flighttime = []
        big_airline = []
        for i in dateAppender(dep_date):
            print(i)
            URL = f'https://www.kayak.com/flights/{departure}-{destination}/{i}?sort=bestflight_a'

            driver.get(URL)
            t.sleep(5)
            big_prov.extend(provider())
            #t.sleep(10)
            big_price.extend(price())
            #t.sleep(10)
#            print(flight_time_and_airline())
            dt, da = flight_time_and_airline()
            big_flighttime.extend(dt)
            big_airline.extend(da)


            db["Provider"] = big_prov
            db["Price"] = big_price
            db["Departure-time"] = big_flighttime
            db["Departure-airline"] = big_airline
        excel(db)


    except Exception as e:
        print(e.args)
    

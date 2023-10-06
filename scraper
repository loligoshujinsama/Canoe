from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time as t
from datetime import *
import sys
import pandas as pda
import openpyxl
from selenium.webdriver.support.select import Select

db={
    "Provider":"",
    "Price":"",
    "Time":"",
    "Airline":"",
    "Date":""
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
        if len(temp)==2:
            dt.append(temp[0])
            da.append(temp[1])
        else:
            dt.append(temp[0])
            da.append(temp[2])
            

    return dt, da

def dateAppender(dep_date):
    format = '%Y-%m-%d'
    dep_date = datetime.strptime(dep_date,format)
    print(dep_date+timedelta(days=30))

    next30=[]
    for i in range(30):
        a = str(dep_date)
        a=a.split(" ")
        next30.append(a[0])
        dep_date = dep_date + timedelta(days=1)
    return next30

def excel(a):
    df = pda.DataFrame(a)
    df.to_excel("output.xlsx")


departure = "SIN"
destination = "BKK"
dep_date = "2023-11-11"

if __name__ == '__main__':
    try:
        a = webdriver.ChromeOptions()
        driver = webdriver.Chrome(a)
        big_prov = []
        big_price = []
        big_flighttime = []
        big_airline = []
        big_date = []

        
        #for i in range(3):
        #    dep_date=dateAppender(dep_date)[-1]
        for i in dateAppender(dep_date):
            print(i)
            URL = f'https://www.kayak.com/flights/{departure}-{destination}/{i}?sort=bestflight_a'
            driver.get(URL)
            t.sleep(5)
            big_prov.extend(provider())
            big_price.extend(price())
            dt, da = flight_time_and_airline()
            big_flighttime.extend(dt)
            big_airline.extend(da)
            for j in range(len(provider())):
                big_date.append(i)

            db["Provider"] = big_prov
            db["Price"] = big_price
            db["Time"] = big_flighttime
            db["Airline"] = big_airline
            db["Date"] = big_date
            #driver.close()
        excel(db)


    except Exception as e:
        print(e.args)
    

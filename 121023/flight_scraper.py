from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
import time as t
from datetime import *
import sys
import pandas as pda
import openpyxl

db = {
    "Provider": "",
    "Price": "",
    "Time": "",
    "Airline": "",
    "Date": ""
}


def provider(driver):
    array_provider = []
    e = driver.find_elements(By.CLASS_NAME, 'M_JD-provider-name')
    e = driver.find_elements(By.CLASS_NAME, 'M_JD-provider-name')
    e = driver.find_elements(By.CLASS_NAME, 'M_JD-provider-name')
    e = driver.find_elements(By.CLASS_NAME, 'M_JD-provider-name')
    for element in e:
        array_provider.append(element.text)
    return array_provider


def price(driver):
    array_price = []
    e = driver.find_elements(By.CLASS_NAME, 'f8F1-price-text')
    e = driver.find_elements(By.CLASS_NAME, 'f8F1-price-text')
    e = driver.find_elements(By.CLASS_NAME, 'f8F1-price-text')
    e = driver.find_elements(By.CLASS_NAME, 'f8F1-price-text')
    for element in e:
        e = element.text.strip("$")
        a = e.replace(",", "")
        array_price.append(int(a))
        # array_price.append(element.text)
    return array_price


def flight_time_and_airline(driver):
    counter = []
    e = driver.find_elements(By.CLASS_NAME, 'VY2U')
    e = driver.find_elements(By.CLASS_NAME, 'VY2U')
    e = driver.find_elements(By.CLASS_NAME, 'VY2U')
    e = driver.find_elements(By.CLASS_NAME, 'VY2U')
    for element in e:
        counter.append(element.text)
        flight_time_departure = []
        for i in range(len(counter)):
            flight_time_departure.append(counter[i])

    # Extract flight time and airline
    dt = []
    da = []

    for i in range(len(flight_time_departure)):
        temp = []
        temp = flight_time_departure[i].split('\n')
        if len(temp) == 2:
            dt.append(temp[0])
            da.append(temp[1])
        else:
            dt.append(temp[0])
            da.append(temp[2])

    return dt, da


###Changes here###
###Debugging####
def dateAppender(dep_date):
    format = '%Y-%m-%d'
    dep_date = datetime.strptime(dep_date, format)

    ### Debugging change duration value
    duration = 2

    dep_date = dep_date + timedelta(days=-7)
    # print(dep_date)
    next = []
    for i in range(duration):
        a = str(dep_date)
        print(a)
        a = a.split(" ")
        next.append(a[0])
        dep_date = dep_date + timedelta(days=1)
    return next


def excel(db):
    df = pda.DataFrame(db)
    return df


def initiateScrape(departure, destination, dep_date):
    chrome_options = Options()

    '''
    user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
    ]
    '''

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
    chrome_options.add_argument("--headless")
    # Cannot do headless user-agent, so we add ourselves :)
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument('--log-level=3')
    driver = webdriver.Chrome(options=chrome_options)
    big_prov = []
    big_price = []
    big_flighttime = []
    big_airline = []
    big_date = []

    for i in dateAppender(dep_date):
        URL = f'https://www.kayak.com/flights/{departure}-{destination}/{i}?sort=bestflight_a'
        driver.get(URL)
        print(i, URL)
        t.sleep(10)
        a = provider(driver)
        big_prov.extend(a)
        t.sleep(5)
        big_price.extend(price(driver))
        print(len(big_price))
        print(len(big_prov))
        t.sleep(5)
        dt, da = flight_time_and_airline(driver)
        t.sleep(5)
        big_flighttime.extend(dt)
        print(len(big_flighttime))
        big_airline.extend(da)
        for j in range(len(a)):
            big_date.append(i)
        t.sleep(5)
        db["Provider"] = big_prov
        db["Price"] = big_price
        db["Time"] = big_flighttime
        db["Airline"] = big_airline
        db["Date"] = big_date
        driver.refresh()
    return db

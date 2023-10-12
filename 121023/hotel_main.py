from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time as t
import pandas as pd
from selenium.webdriver.support.select import Select
from wordcloud import WordCloud
import os
from datetime import *
from pathlib import Path

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
STATIC_PATH = CURRENT_PATH + r'\static'
PICTURE = Path(STATIC_PATH) / 'CLOUDHotelBasedOnRating.png'

# Will need to change these values in future, now is just for testing purposes
# Format is: YYYY-MM-DD
# hazel will pass me destination
# hazel will pass me end_date, and i need to decrement by 1 day
# start_date = "2024-06-23"
# end_date = "2024-06-24"
# destination = "seoul"
# url = f"https://www.expedia.com.sg/Hotel-Search?adults=1&children=&destination={destination}&endDate={end_date}&startDate={start_date}"


def initialize_driver():
    options = Options()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
    # options.add_argument("--headless=new")
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--log-level=3')
    driver = webdriver.Chrome(options=options)
    return driver


def scrape_hotel_data(driver, destination, date):
    format = '%Y-%m-%d'
    a = datetime.strptime(date, format)
    end_date = str(a).split(' ')[0]
    start_date = a + timedelta(days=-1)
    start_date = str(start_date).split(' ')
    url = f"https://www.expedia.com.sg/Hotel-Search?adults=1&children=&destination={destination}&endDate={end_date}&startDate={start_date[0]}"
    driver.get(url)
    print(url)
    t.sleep(40)

    name_list = []
    price_list = []
    rating_list = []

    # search for all hotels based on the XPATH tied to each hotel block
    hotel_elements = driver.find_elements(By.XPATH,
                                          "//div[@class='uitk-layout-flex uitk-layout-flex-block-size-full-size uitk-layout-flex-flex-direction-column uitk-layout-flex-justify-content-space-between']")

    # extract each hotel's name, price and rating under the hotel block
    for hotel_element in hotel_elements:
        try:
            hotel_name = hotel_element.find_element(By.XPATH,
                                                    ".//h3[@class='uitk-heading uitk-heading-5 overflow-wrap uitk-layout-grid-item uitk-layout-grid-item-has-row-start']")

            hotel_price = hotel_element.find_element(By.XPATH,
                                                     ".//div[@class='uitk-text uitk-type-500 uitk-type-medium uitk-text-emphasis-theme']")
            price = hotel_price.text if hotel_price else 'Sold out'

            hotel_rating = hotel_element.find_elements(By.XPATH, ".//span[@class='uitk-badge-base-text']")
            rating = hotel_rating[0].text if hotel_rating else 'No ratings found'

            name_list.append(hotel_name.text)
            price_list.append(price)
            rating_list.append(rating)
        # if hotel is sold out, just ignore the data for that hotel and carry on
        except NoSuchElementException:
            pass

    return name_list, price_list, rating_list


def generate_word_cloud(words):
    # Create a WordCloud object
    wordcloud = WordCloud(max_font_size=75)

    # Generate the word cloud from the list of words
    wordcloud.generate_from_frequencies(words)

    # Return the word cloud object
    return wordcloud


def WCHotelRating(df):
    WCDic = {}
    WCDic = df.to_dict()
    ListOfHotels = []
    ListOfHotels = WCDic.get("hotel_name")
    ListOfHotels = [value for value in ListOfHotels.values()]
    ListOfHotelRatings = []
    ListOfHotelRatings = WCDic.get("hotel_rating")
    ListOfHotelRatings = [value for value in ListOfHotelRatings.values()]

    # Edit out bad records

    ListOfHotelsCLEANED = []
    ListOfHotelRatingsCLEANED = []
    for eachhotel in range(len(ListOfHotels)):
        if ListOfHotelRatings[eachhotel] != "No ratings found":
            ListOfHotelsCLEANED.append(ListOfHotels[eachhotel])
            ListOfHotelRatingsCLEANED.append(float(ListOfHotelRatings[eachhotel]))

    # Combine both list into dic
    mydic = dict(zip(ListOfHotelsCLEANED, ListOfHotelRatingsCLEANED))
    wordcloud3 = generate_word_cloud(mydic)
    # wordcloud3.to_file("CLOUDHotelBasedOnRating.png")
    wordcloud3.to_file(str(PICTURE))



def excel(data):
    db = {
        "hotel_name": data[0],
        "hotel_price": data[1],
        "hotel_rating": data[2]
    }
    df = pd.DataFrame(db)
    WCHotelRating(df)
    # top10_dic = {}
    # top10_dic = gettop10(df)
    l1 = []
    l2 = []
    l1, l2 = gettop10(df)
    # print(top10_dic)
    return l1, l2


def gettop10(df):
    DicOfRatings = {}
    DicOfRatings = df.to_dict()
    ListOfHotels = []
    ListOfHotels = DicOfRatings.get("hotel_name")
    ListOfHotels = [value for value in ListOfHotels.values()]
    ListOfHotelRatings = []
    ListOfHotelRatings = DicOfRatings.get("hotel_rating")
    ListOfHotelRatings = [value for value in ListOfHotelRatings.values()]
    ListOfHotelPrice = []
    ListOfHotelPrice = DicOfRatings.get("hotel_price")
    ListOfHotelPrice = [value for value in ListOfHotelPrice.values()]

    ListTo2ndSortRATING = []
    ListTo2ndSortHOTELNAME = []
    ListTo2ndSortPRICE = []
    # First Sort
    Base = 5

    for x in range(len(ListOfHotelRatings)):
        if ListOfHotelRatings[x] != "No ratings found":
            if float(ListOfHotelRatings[x]) > Base:
                # Base = float(ListOfHotelRatings[x])
                ListTo2ndSortRATING.append(ListOfHotelRatings[x])
                ListTo2ndSortPRICE.append(ListOfHotelPrice[x])
                ListTo2ndSortHOTELNAME.append(ListOfHotels[x])

    # print(ListTo2ndSortPRICE, ListTo2ndSortRATING, ListTo2ndSortHOTELNAME)
    # combine all 2 first to a dic maybe and compare?
    Dic2 = dict(zip(ListTo2ndSortHOTELNAME, ListTo2ndSortRATING))
    Dic2Sprted = {}
    Dic2Sprted = sorted(Dic2.items(), key=lambda item: item[1], reverse=True)
    Dic3Sprted = {}
    Dic3Sprted = {key: value for key, value in enumerate(Dic2Sprted) if key < 10}
    print(Dic3Sprted)
    hotelnamelist = list(Dic3Sprted.keys())
    hotelratinglist = list(Dic3Sprted.values())
    return hotelnamelist, hotelratinglist


def main():
    driver = initialize_driver()
    hotel_data = scrape_hotel_data(initialize_driver(), destination="Bahrain", date="2024-03-02")
    main_dic = {}
    main_dic = excel(hotel_data)
    driver.quit()


if __name__ == "__main__":
    main()

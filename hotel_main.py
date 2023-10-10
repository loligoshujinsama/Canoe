from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time as t
import pandas as pd
from selenium.webdriver.support.select import Select
from wordcloud import WordCloud

#Will need to change these values in future, now is just for testing purposes
#Format is: YYYY-MM-DD
start_date = "2024-07-25"
end_date = "2024-07-29"
destination = "bahrain"
url = f"https://www.expedia.com.sg/Hotel-Search?adults=1&children=&destination={destination}&endDate={end_date}&startDate={start_date}"

def initialize_driver():
    options = Options()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    options.add_argument("--headless=new")
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--log-level=3')
    driver = webdriver.Chrome(options=options)
    return driver

def scrape_hotel_data(driver):
    driver.get(url)
    t.sleep(10)

    name_list = []
    price_list = []
    rating_list = []

    hotel_elements = driver.find_elements(By.XPATH, "//div[@class='uitk-layout-flex uitk-layout-flex-block-size-full-size uitk-layout-flex-flex-direction-column uitk-layout-flex-justify-content-space-between']")
    
    for hotel_element in hotel_elements:
        try:
            hotel_name = hotel_element.find_element(By.XPATH, ".//h3[@class='uitk-heading uitk-heading-5 overflow-wrap uitk-layout-grid-item uitk-layout-grid-item-has-row-start']")

            hotel_price = hotel_element.find_element(By.XPATH, ".//div[@class='uitk-text uitk-type-500 uitk-type-medium uitk-text-emphasis-theme']")
            price = hotel_price.text if hotel_price else 'Sold out'
            
            hotel_rating = hotel_element.find_elements(By.XPATH, ".//span[@class='uitk-badge-base-text']")
            rating = hotel_rating[0].text if hotel_rating else 'No ratings found'

            name_list.append(hotel_name.text)
            price_list.append(price)
            rating_list.append(rating)
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
    #df = pd.read_excel("hotel.xlsx", index_col=0)
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
    wordcloud3.to_file("CLOUDHotelBasedOnRating.png")
    
def excel(data):
    db = {
        "hotel_name": data[0],
        "hotel_price": data[1],
        "hotel_rating": data[2]
    }
    df = pd.DataFrame(db)
    WCHotelRating(df)
    #df.to_excel("hotel.xlsx")

def main():
    driver = initialize_driver()
    hotel_data = scrape_hotel_data(driver)
    excel(hotel_data)
    driver.quit()

if __name__ == "__main__":
    main()

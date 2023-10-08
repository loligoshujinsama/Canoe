from flight_scraper import *
from airline_review import *
# from predictive_analysis import * 
# from line_graph import *


departure = "SIN" # Only SIN
destination = "BKK" # User to select
dep_date = "2023-11-13" # Based on which race selected

#Return dataframe from scraping hotel
dict = initiateScrape(departure, destination, dep_date)
# dataframe = excel(dict)
# print(dataframe)

# Hotel reviews will be based on the airline fetched by scraper
print(fetchAirlineReview(dict))

# Graphs to run before main.py
# 1. Predictive analysis
# predictiveB(clean()) 

# 2. Plot the line graph
# plot_linegraph(dataframe)



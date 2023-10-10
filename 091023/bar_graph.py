import pandas as pd
import openpyxl
import plotly.graph_objects as go
#import flight_scraper
from datetime import *
MONTH_DICTIONARY={1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}


def custom_median(values):
    """
    This function will sort a list of numbers and return the lower middle value of the list.
    e.g.: [1,2,3] will return 2; [1,2,3,4] will return 2; [2,1,41,4,5] --> [1,2,4,5,41] will return 4
    """

    sorted_prices = sorted(values)
    n = len(sorted_prices)
    if n % 2 == 1:
        return sorted_prices[n // 2]        # Return the middle value e.g.: [1,2,3] --> 2
    return sorted_prices[n // 2 - 1]        # Return the lower middle value e.g.: [1,2,3,4] --> 2


def read_excel_file(dataframe, month):
    """
    This function takes in a dataframe as a parameter and groups them by airline
    It returns the sorted dataframe as well as the miniumum and maximum value
    """
    return dataframe.apply(custom_median).reset_index()
    

def bargraph(df, cheap, expensive):
    """
    This function takes in a dataframe and 
    plots a horizontal bar graph for a given month
    where the x axis is the price of the flight
    and the y axis indicates the type of airline
    """

    fig = go.Figure()
    add_min_max(df, cheap, expensive)
    cheap_prices = df['min']
    expensive_prices = df['max']
    annotations = ['min', 'max']
    fig.add_trace(go.Bar(
        y=df['Airline'],
        x=df['Price'],
        textposition = "none",
        orientation='h',
    ))


    fig.update_traces(text=df['min'], 
        textposition='inside')
    fig.update_layout(
        title=f'Airline average prices',
        xaxis_title='Price',
        yaxis_title='Airline',
    )
    
    fig.write_html(r"C:\Users\Lucas\PycharmProjects\ICT1002_Assignment\venv\bar_graphtest.html")


def add_min_max(dataframe, cheapest, expensive):
    """
    This function appends the cheapest and most expensive flight to the dataframe
    """
    cheap_list = str(cheapest).split()
    expensive_list = str(expensive).split()
    cheap_prices = [number for number in cheap_list if number.isdigit()]
    expensive_prices = [number for number in expensive_list if number.isdigit()]
    dataframe['min'] = cheap_prices
    dataframe['max'] = expensive_prices

    return dataframe


def plot_bargraph(data, month):
    """
    This function will only run if and only if it is NOT IMPORTED as a module.
    """
    airline_data = data.groupby('Airline')['Price']
    data_frame = read_excel_file(airline_data, month)

    bargraph(data_frame, airline_data.min(), airline_data.max())


# df = pd.read_excel(r'C:\Users\Lucas\PycharmProjects\ICT1002_Assignment\venv\scraped.xlsx', engine='openpyxl')
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', 2000)
# pd.set_option('display.float_format', '{:20,.2f}'.format)
# pd.set_option('display.max_colwidth', None)
# plot_bargraph(df, 10)

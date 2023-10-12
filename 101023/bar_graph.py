import pandas as pd
import openpyxl
import plotly.graph_objects as go
from datetime import *
import os
from pathlib import Path

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
STATIC_PATH = CURRENT_PATH + r'\static'
HTML_GRAPH = Path(STATIC_PATH) / 'bar_graphtest.html'
TAB = '    '
#HTML_GRAPH = r"C:\Users\Lucas\PycharmProjects\ICT1002_Assignment\venv\real\static\bar_graphtest.html"  # CHANGE THIS


def custom_median(values):
    """
    This function will sort a list of numbers and return the lower middle value of the list.
    e.g.: [1,2,3] will return 2; [1,2,3,4] will return 2; [2,1,41,4,5] --> [1,2,4,5,41] will return 4
    """

    sorted_prices = sorted(values)
    n = len(sorted_prices)
    if n % 2 == 1:
        return sorted_prices[n // 2]  # Return the middle value e.g.: [1,2,3] --> 2
    return sorted_prices[n // 2 - 1]  # Return the lower middle value e.g.: [1,2,3,4] --> 2


def bargraph(df, cheap, expensive):
    """
    This function takes in a dataframe and 
    plots a horizontal bar graph for a given month
    where the x axis is the price of the flight
    and the y axis indicates the type of airline
    additional information such as the cheapest and
    most expensive flight is also provided.
    """
    
    fig = go.Figure()
    add_min_max(df, cheap, expensive)
    cheap_prices = df['min']
    expensive_prices = df['max']
    fig.add_trace(go.Bar(
        y=df['Airline'],    
        x=df['Price'],
        orientation='h',
    ))
    #This block of code annotates on each bar the cheapest & most expensive flight for each airline
    fig.update_traces(
        text=TAB + TAB + 'Cheapest flight: $' + cheap_prices + TAB + 'Most expensive flight: $' + expensive_prices,
        textposition='inside',
        insidetextanchor='start'
    )
    #This block of code labels the x, y axis and the graph
    fig.update_layout(
        title=f'Airline average prices',
        xaxis_title='Price ($)',
        yaxis_title='Airline',
    )

    fig.write_html(HTML_GRAPH)


def add_min_max(dataframe, cheapest, expensive):
    """
    This function appends the cheapest and most expensive flight to the dataframe
    """
    cheap_list = str(cheapest).split()
    expensive_list = str(expensive).split()
    dataframe['min'] = [number for number in cheap_list if number.isdigit()]
    dataframe['max'] = [number for number in expensive_list if number.isdigit()]


def plot_bargraph(data):
    """
    This function outlines the logic behind plotting the bargraph
    """
    airline_data_median = data.groupby('Airline')['Price'].apply(custom_median).reset_index()
    airline_data = data.groupby('Airline')['Price']

    bargraph(airline_data_median, airline_data.min(), airline_data.max())


# Anything below this comment is plainly for debugging purposes ONLY :) 

# df = pd.read_excel(r'C:\Users\Lucas\PycharmProjects\ICT1002_Assignment\venv\101023\scraped.xlsx', engine='openpyxl')
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', 2000)
# pd.set_option('display.float_format', '{:20,.2f}'.format)
# pd.set_option('display.max_colwidth', None)
# plot_bargraph(df)

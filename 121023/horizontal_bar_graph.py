import pandas as pd
import openpyxl
import plotly.graph_objects as go
from datetime import *

MONTH_DICTIONARY={1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}


"""
+=+=+=+=+=+=IMPORTANT+=+=+=+=+=+=
Ensure that the month is an INTEGER before using any of the functions in this module :D
"""


def filter_month(dataframe, month):
    """
    This function changes the date format to only include the month as an integer.
    e.g.: [2023-10-23 ---> 10] ; [2023-01-12] ---> 1] ; [2024-09-29 ---> 9]
    After which it will only keep the rows relevant to the specified month in the params.
    e.g.: month == 9 ; returned df will ONLY contain rows with the number 9 in the date column
    """

    df = dataframe
    format = '%Y-%m-%d'                                                     # Specify a time format
    for i in range(len(dataframe['Date'])):
        try:
            month_in_number = datetime.strptime(df['Date'][i], format)
            df.Date[df.Date == df['Date'][i]] = month_in_number.month       # Change 23-01-12 to 1
        except: 
            pass
    return df[df['Date'] == month]                                          # Keep data relevant to the specified month


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
    This function takes in the excel file as a parameter and will
    convert it into a dataframe using the pandas module
    """

    # dataframe = pd.read_excel(EXCEL_FILE, engine='openpyxl')
    print(dataframe)
    # dataframe['Price'] = pd.to_numeric(dataframe['Price'].str.replace('$', '').str.replace(',', ''))    # Removes the $ from $100

    # median_prices_dataframe = dataframe.groupby('airline')['Price'].apply(custom_median).reset_index()  # Consolidate median data
    working_df = filter_month(dataframe, month)
    return working_df.groupby('Airline')['Price'].apply(custom_median).reset_index()
    

def horizontal_bar_graph(df,month):
    """
    This function takes in a dataframe and 
    plots a horizontal bar graph for a given month
    where the x axis is the price of the flight
    and the y axis indicates the type of airline
    """

    fig = go.Figure()
    displaying_month = MONTH_DICTIONARY[month]
    fig.add_trace(go.Bar(
        y=df['Airline'],
        x=df['Price'],
        orientation='h',
    ))

    fig.update_layout(
        title=f'Price by airline for the month of {displaying_month}',
        xaxis_title='Price',
        yaxis_title='Airline',
    )
    # fig.show()              #This line of code pops up the graph. It may be redundant if you want to save as html
    fig.write_html(r"C:\Users\brand\PycharmProjects\pythonProject\091023\091023\templates\line_graphtest.html")

def main(data, month):
    """
    This function will only run if and only if it is NOT IMPORTED as a module.
    """

    data_frame = read_excel_file(data, 10)
    horizontal_bar_graph(data_frame, 10)




if __name__ == "__main__":
    main()

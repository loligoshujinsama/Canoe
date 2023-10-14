import pandas as pd
import openpyxl
import plotly.graph_objects as go
import os
from pathlib import Path

STATIC_PATH = os.path.dirname(os.path.abspath(__file__)) + r'\static'
HTML_FILE = Path(STATIC_PATH) / 'line_graphtest.html'

### Point to the excel (Debugging) ###
# EXCEL_FILE = r'H:/scraped.xlsx'


def custom_median(values):
    """
    This function returns the lower middle value of the list.
    e.g.: [1,2,3] will return 2;    [1,2,3,4] will return 2; [1,2,3,4,5] will return 3
    """
    sorted_prices = sorted(values)
    n = len(sorted_prices)
    if n % 2 == 1:
        return sorted_prices[n // 2]
    return sorted_prices[n // 2 - 1]


def plot_linegraph(dataframe):
    """
    This function takes in a dataframe and plots a line graph using
    the column values of 'Price', 'Date' and 'Airline'. After which
    it will save the graph object into a HTML file.
    """
    median_prices_dataframe = dataframe.groupby('Date')['Price'].apply(custom_median).reset_index()

    merged_df = pd.merge(median_prices_dataframe, dataframe, on=['Date', 'Price'], how='left')
    #Add a hover over box that shows airline, provider, and price
    merged_df['hover_text'] = merged_df.apply(
        lambda row: f"Airline: {row['Airline']}<br>Provider: {row['Provider']}<br>Price: {row['Price']}", axis=1)

    merged_df['Airline'].fillna('N/A', inplace=True)
    merged_df['Provider'].fillna('N/A', inplace=True)
    fig = go.Figure()
    #Plot a line graph where the date and price represent the x and y axis respectively
    fig.add_trace(go.Scatter(x=merged_df['Date'], y=merged_df['Price'], mode='lines', name='Trend'))
    # Add airline name when hovering over a plotted point
    fig.add_trace(go.Scatter(x=merged_df['Date'], y=merged_df['Price'], mode='markers', name='Median Price',
                             marker=dict(color='grey', size=8), hovertext=merged_df['hover_text'], hoverinfo='text'))

    fig.update_xaxes(tickvals=merged_df['Date'], tickformat='%Y-%m-%d', title_text='Date')
    fig.update_yaxes(title_text='Price')
    fig.write_html(HTML_FILE)                #Save graph object into a HTML file.



#if __name__ == '__main__':
#    main()

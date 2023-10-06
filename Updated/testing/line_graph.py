import pandas as pd
import openpyxl
import plotly.graph_objects as go
import mpld3


EXCEL_FILE = r'C:\Users\brand\scraped.xlsx'


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


def main(dataframe):
    # dataframe = pd.read_excel(filename, engine='openpyxl')
    # pd.set_option('display.max_rows', 500)
    # pd.set_option('display.max_columns', 500)
    # pd.set_option('display.width', 300)

    dataframe['Price'] = pd.to_numeric(dataframe['Price'].str.replace('$', '').str.replace(',', ''))
    median_prices_dataframe = dataframe.groupby('Date')['Price'].apply(custom_median).reset_index()

    merged_df = pd.merge(median_prices_dataframe, dataframe, on=['Date', 'Price'], how='left')

    merged_df['hover_text'] = merged_df.apply(
        lambda row: f"Airline: {row['Airline']}<br>Provider: {row['Provider']}<br>Price: {row['Price']}", axis=1)

    merged_df['Airline'].fillna('N/A', inplace=True)
    merged_df['Provider'].fillna('N/A', inplace=True)
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=merged_df['Date'], y=merged_df['Price'], mode='lines', name='Trend'))

    fig.add_trace(go.Scatter(x=merged_df['Date'], y=merged_df['Price'], mode='markers', name='Median Price',
                             marker=dict(color='grey', size=8), hovertext=merged_df['hover_text'], hoverinfo='text'))

    fig.update_xaxes(tickvals=merged_df['Date'], tickformat='%Y-%m-%d', title_text='Date')
    fig.update_yaxes(title_text='Price')

    fig.write_html(r"C:\Users\brand\PycharmProjects\pythonProject\templates\line_graphtest.html")
    # interactivePlot = mpld3.fig_to_html(fig)
    #
    # return interactivePlot


# if __name__ == '__main__':
#     main()

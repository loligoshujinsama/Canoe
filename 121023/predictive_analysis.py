import pandas as pda
import matplotlib.pyplot as plt
import numpy as np
from ggplot import *
import warnings

warnings.filterwarnings('ignore')
from sklearn.linear_model import LinearRegression
from prophet import Prophet
# from prophet.plot import add_changepoints_to_plot
import plotly.graph_objects as go
import os
from pathlib import Path

STATIC_PATH = os.path.dirname(os.path.abspath(__file__)) + r'\static'
HTML_FILE = Path(STATIC_PATH) / 'predictive_analysis.html'


def clean():
    data = pda.read_csv("M650041.csv")
    a = data.iloc[9]
    b = data.iloc[8]
    train_month = []
    train_values = []
    valid_month = []
    valid_values = []

    # Trying to avoid COVID period as it deflates values (hard-coded)
    n = 1
    for i in range(n + 104, n + 130):
        train_month.append(b[i])
        train_values.append(int(a[i]))
    # 50,76 & 104,130 is good.
    for i in range(1, 27):
        valid_month.append(b[i])
        valid_values.append(int(a[i]))
    return train_month, train_values, valid_month, valid_values


def predictiveA(list):
    ### LINEAR REGRESSION ###
    df = pda.DataFrame(list[:4]).transpose()
    df.columns = ['train_month', 'train_departures', 'valid_month', 'valid_departures']
    df["train_departures"] = df["train_departures"].astype(np.int64)
    # df['train_estimationDep'] =  round((df['train_departures']),-4)
    df['train_month'] = pda.to_datetime(df['train_month'])

    df["valid_departures"] = df["valid_departures"].astype(np.int64)
    # df['valid_estimationDep'] =  round((df['valid_departures']),-4)
    df["valid_month"] = pda.to_datetime(df['valid_month'])

    ### Creates new column 'predictive'. Takes the average of train and valid ###
    df["predictive"] = (df["valid_departures"] + df["train_departures"]) / 2

    # Display in millions
    df["valid_departures"] = df["valid_departures"] / 1e9
    df["train_departures"] = df["train_departures"] / 1e9

    # Calculation of MAPE
    ape = []
    ## Creates new column 'ape'. Takes the disparity b/w train and valid 
    df["ape"] = abs((df["train_departures"] - df["valid_departures"]) / df["train_departures"])
    for i in df["ape"]:
        ape.append(i)
    mape = sum(ape) / len(ape)
    mape_percent = round(mape * 100, 2)

    # Forecast of prediction, COVID. Estimation method MAPE (Multiplicative model)
    # Since took abs of disparity, maps 2 lines where it is mape_percent ABOVE or BELOW the actual
    df["forecast-pos"] = df["valid_departures"] + (df["valid_departures"] / 100 * mape_percent)
    df["forecast-neg"] = df["valid_departures"] - (df["valid_departures"] / 100 * mape_percent)

    '''
    #To change the months to this coming 2024 years where applicable, show past, 2023, and 2024
    model = LinearRegression()
    df['valid_month_ordinal'] = df['valid_month'].apply(lambda x: x.toordinal())
    X = df['valid_month_ordinal'].values.reshape(-1, 1)
    Y = df['predictive'].values
    model.fit(X, Y)
    predictions = model.predict(X)

    plt.figure(figsize=(10, 8))
    plt.plot(df['valid_month'], predictions, 'm-', label = 'predictions')
    plt.plot(df['valid_month'], df['forecast-neg'], 'b-', label = 'forecast-neg', linestyle = "-")
    plt.plot(df['valid_month'], df['forecast-pos'], 'r-', label = 'forecast-pos', linestyle = "-")
    plt.plot(df['valid_month'], df['valid_departures'], 'g-', label = 'valid_departures', linestyle = "--")
    plt.plot(df['valid_month'], df['train_departures'], 'c-', label = 'train_departures', linestyle = "--")
    plt.xlabel('valid_month');plt.ylabel('Forecast of flight departures (global)');plt.title('Bookings per month (in millions)')
    plt.legend()
    #plt.show()
    '''


def predictiveB(list):
    ### PROPHET ###
    # df2 is DataFrame in-use for Prophet
    df2 = pda.DataFrame(list[2:4]).transpose()
    df2.columns = ['valid_month', 'valid_departures']
    df2["valid_departures"] = df2["valid_departures"].astype(np.int64) / 1e6
    df2["valid_month"] = pda.to_datetime(df2['valid_month'])

    a = df2.rename(columns={'valid_month': 'ds', 'valid_departures': 'y'})

    '''
    #####################
    ### Training Data ###
    #####################
    ax = a.set_index('ds').plot(figsize=(12, 8))
    ax.set_ylabel('Monthly Number of Airline Passengers')
    ax.set_xlabel('Date')
    '''

    model = Prophet(interval_width=0.8)
    model.fit(a)

    # To update this one
    future_dates = model.make_future_dataframe(periods=16, freq='MS')
    # print(future_dates)

    forecast = model.predict(future_dates)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=a['ds'], y=a['y'], mode='lines', name='Actual'))
    # forecast[['ds','yhat','yhat_lower','yhat_upper']]

    # fig = model.plot(forecast, uncertainty=True)
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecast'))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], mode='lines', name='Lower Bound'))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], mode='lines', name='Upper Bound'))

    model.plot_components(forecast)

    # Line trend
    # a = add_changepoints_to_plot(fig.gca(), model, #forecast)
    # print(model.changepoints)
    fig.write_html(HTML_FILE)

import pandas as pda
import matplotlib.pyplot as plt
import numpy as np
from ggplot import *
import warnings
warnings.filterwarnings('ignore')
from prophet import Prophet
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

    # Trying to avoid COVID period as it deflates values
    # Training data
    n = 1
    for i in range(n + 104, n + 130):
        train_month.append(b[i])
        train_values.append(int(a[i]))
    # Valid data
    # 50,76 & 104,130 is good.
    for i in range(1, 27):
        valid_month.append(b[i])
        valid_values.append(int(a[i]))
    return train_month, train_values, valid_month, valid_values

def predictiveB(list):
    '''
    Initialise prophet to start forecasting. Takes in cleaned list of training and valid datasets.
    '''

    ### PROPHET ###
    df2 = pda.DataFrame(list[2:4]).transpose()
    df2.columns = ['valid_month', 'valid_departures']
    df2["valid_departures"] = df2["valid_departures"].astype(np.int64) / 1e6
    df2["valid_month"] = pda.to_datetime(df2['valid_month'])

    a = df2.rename(columns={'valid_month': 'ds', 'valid_departures': 'y'})

    # Start Prophet
    model = Prophet(interval_width=0.8)
    model.fit(a)

    # Adjust future period
    future_dates = model.make_future_dataframe(periods=16, freq='MS')

    # Predictions and plotting
    forecast = model.predict(future_dates)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=a['ds'], y=a['y'], mode='lines', name='Actual'))

    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecast'))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], mode='lines', name='Lower Bound'))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], mode='lines', name='Upper Bound'))
    fig.update_layout(title='Forecasted total number of global departures (in millions)')
    model.plot_components(forecast)

    fig.write_html(HTML_FILE)

if __name__ == "__main__":
    predictiveB(clean())

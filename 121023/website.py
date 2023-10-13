from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
import requests
import os
import bar_graph
import line_graph
import flight_scraper
import natural_lang
import airline_review
import predictive_analysis
import hotel_main
import pandas as pda
from datetime import date

app = Flask(__name__, template_folder='templates')

location = {
      'BAH':"2024-03-02",
      'JED':"2024-03-09",
      "MEL":"2024-03-24",
      'TYO':"2024-04-07",
      'SHA':"2024-04-21",
      'MIA':"2024-05-05",
      'BLQ':"2024-05-19",
      "NCE":"2024-05-26",
      "YMQ":"2024-06-09",
      "BCN":"2024-06-23",
      "GRZ":"2024-06-30",
      "LHR":"2024-07-07",
      "BUD":"2024-07-21",
      "LGG":"2024-07-28",
      "AMS":"2024-08-25",
      "LIN":"2024-09-01",
      "BAK":"2024-09-15",
      "SIN":"2024-09-22",
      "AUS":"2024-10-20",
      "TLC":"2024-10-27",
      "SAO":"2024-11-03",
      "LAS":"2024-11-23",
      "DOH":"2024-12-01",
      "AUH":"2024-12-08"
}

mapper = {
    'BAH':'bahrain',
    'JED':'jeddah',
    'MEL':'melbourne',
    'TYO':'tokyo',
    'SHA':'shanghai',
    'MIA':'miami',
    'BLQ':'imola',
    'NCE':'monaco',
    'YMQ':'montreal',
    'BCN':'barcelona',
    'GRZ':'spielberg',
    'LHR':'silverstone',
    'BUD':'budapest',
    'LGG':'liege',
    'AMS':'amsterdam',
    'LIN':'monza',
    'BAK':'baku',
    'SIN':'singapore',
    'AUS':'austin',
    'TLC':'mexico-city',
    'SAO':'sao-paolo',
    'LAS':'las-vegas',
    'DOH':'lusail',
    'AUH':'yas-marina'
}

@app.route("/")
def home():
    return render_template('homepage.html')


departure = "SIN"
destination = ""
dep_date = ""


@app.route("/", methods=(['GET', 'POST']))
def result():
    if request.method == 'POST':
        global departure
        global destination
        global dep_date

        destination = request.form.get("dest")
        dep_date = request.form.get("date")

    print("Chosen destination: "+ mapper[destination])
    global dict
    dict = flight_scraper.initiateScrape(departure, request.form["dest"], location[request.form["dest"]])
    df = flight_scraper.excel(dict)
    line_graph.plot_linegraph(df)
    bar_graph.plot_bargraph(df)
    #predictive_analysis.predictiveB(predictive_analysis.clean())
    list_for_html = airline_review.fetchAirlineReview(dict)[1]

    return render_template("display.html", list_for_html = list_for_html, destination=destination)



@app.route("/")
def linegraph():
    return render_template('line_graphtest.html')


@app.route("/")
def bargraph():
    return render_template('bar_graph.html')


@app.route("/")
def predictive():
    return render_template('predictive_analysis.html')

@app.route('/wordcloud/<item>')
def wordcloud(item):
    natural_lang.initiateNLP(dict, item)
    image = f'static/{item}.png'
    return send_file(image, mimetype= 'image/png')

@app.route("/next")
def hotel_page():
    hotel_data = hotel_main.scrape_hotel_data(hotel_main.initialize_driver(), mapper[destination], dep_date)
    l1 = []
    l2 = []
    l1,l2 = hotel_main.excel(hotel_data)
    return render_template("hotel_page.html", l1=l1, l2=l2)

if __name__ == "__main__":
    app.run()

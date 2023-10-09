from flask import Flask, render_template, request
import requests
import bar_graph
import line_graph
import flight_scraper
import natural_lang
import airline_review
import pandas as pda
from datetime import date

app = Flask(__name__, template_folder='templates')

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

    dict = flight_scraper.initiateScrape(departure, destination, dep_date)
    df = flight_scraper.excel(dict)
    line_graph.plot_linegraph(df)
    bar_graph.plot_bargraph(df, month=10)
    return render_template("display.html")

@app.route("/")
def linegraph():
    return render_template('line_graphtest.html')

@app.route("/")
def bargraph():
    return render_template('bar_graph.html')

@app.route("/")
def predictive():
    return render_template('predictive_analysis.html')

if __name__ == "__main__":
    app.run()
    

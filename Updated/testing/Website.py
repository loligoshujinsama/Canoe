from flask import Flask, render_template, request
import requests

import horizontal_bar_graph
import line_graph
import scraper
from datetime import date

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('Flight Website.html')


departure = ""
destination = ""
dep_date = ""


@app.route("/", methods=(['GET', 'POST']))
def result():
    if request.method == 'POST':
        global departure
        global destination
        global dep_date

        departure = request.form.get("depart")
        destination = request.form.get("dest")
        dep_date = request.form.get("date").split('-')
        # dep_date = request.form.get("date")

        year, month, day = [int(item) for item in dep_date]
        d = date(year, month, day)

        # return render_template("Flight Website.html")
    # return scraper.testing(departure, destination, dep_date)
    # scraper.testing(departure, destination, d)
    data = scraper.testing(departure, destination, d)
    line_graph.main(data)
    horizontal_bar_graph.main(data, month=10) # to add month in

    return render_template("display.html")


     # user_input = request.form['submit']


# @app.route("/results/")
# def graph():
# return render_template('line_graph.html')


if __name__ == "__main__":
    app.run(debug=True)

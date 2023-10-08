import pandas as pda

# Feed the db created by mainscraper
def fetchAirlineReview(dict):
    unique_airline = []
    for i in dict['Airline']:
        if i in unique_airline:
            pass
        else:
            unique_airline.append(i)

    reviews = {}
    data = pda.read_csv("AirlineReviews.csv")

    for i in unique_airline:
        reviews[i] = data.loc[data['AirlineName'].str.contains(i),'Review'].astype(str).tolist()
    
    return reviews


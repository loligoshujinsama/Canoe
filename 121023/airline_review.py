import pandas as pda


# Feed the db created by mainscraper
# Return as a dictionary
def fetchAirlineReview(dict):
    unique_airline = []
    for i in dict['Airline']:
        if i in unique_airline:
            pass
        else:
            if i == 'Multiple airlines'in i:
                pass
            elif ',' in i:
                i = i.split(', ')
                for i2 in i:
                    if i2 in unique_airline:
                        pass
                    else:
                        unique_airline.append(i2)
            else:
                unique_airline.append(i)

    reviews = {}
    data = pda.read_csv("AirlineReviews.csv")

    for i in unique_airline:
        reviews[i] = data.loc[data['AirlineName'].str.contains(i), 'Review'].astype(str).tolist()

    return reviews, unique_airline


if __name__ == "__main__":
    print(fetchAirlineReview(dict))

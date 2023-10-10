import pandas as pda

# Feed the db created by mainscraper
# Return as a dictionary
def fetchAirlineReview(dict):
    unique_airline = []
    for i in dict['Airline']:
        if i in unique_airline:
            pass
        else:
            if ',' in i:
                i = i.split(', ')
                unique_airline.append(i[0])
                unique_airline.append(i[1])
            elif i == 'Multiple airlines':
                pass
            else:
                unique_airline.append(i)
            

    reviews = {}
    data = pda.read_csv("AirlineReviews.csv")

    for i in unique_airline:
        reviews[i] = data.loc[data['AirlineName'].str.contains(i),'Review'].astype(str).tolist()
    
    return reviews, unique_airline

if __name__ == "__main__":
    print(fetchAirlineReview(dict))

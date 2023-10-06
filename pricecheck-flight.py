import pandas as pd
import heapq

def priceCheck(priceList):
    avg = 0
    for i in priceList:
        avg += i
    avg /= len(priceList)
    return avg, max(priceList), min(priceList)

def searcher(x):
    for i in range(len(priceList)):
        if priceList[i] == x:
            print(df.loc[i])
    
def airlineMedian(df):
    airlines = []
    big_airlines = {}

    for i in df['Airline']:
        if i not in airlines:
            airlines.append(i)
            
    for i in airlines:
        big_airlines[i] = ""

    for i in airlines:
        big_prices = []
        for i2 in range(len(df)):
            if df['Airline'][i2] == i:
                big_prices.append(priceList[i2])
                big_airlines[i] = big_prices
    
    
    for i in airlines:
        a = sorted(big_airlines[i], reverse=False)
        mid = len(big_airlines[i])//2
        if len(big_airlines[i]) % 2 == 0:
            big_airlines[i] = heapq.nlargest(mid,a)[-1] + heapq.nsmallest(mid,a)[-1]/2
        else:
           big_airlines[i] = heapq.nlargest(mid+1, a)[-1]

    return big_airlines

if __name__ == '__main__':
    try:
        file = 'output.xlsx'
        df = pd.read_excel(file)
        priceList = []

        for i in df['Price']:
            priceList.append(int(i.strip('$')))

        avg, max, min = priceCheck(priceList)
        print(searcher(max))
        print(searcher(min))
        print(f"Average: ${avg:.2f}")
        print(airlineMedian(df))


    except Exception as e:
        print(e.args)
    

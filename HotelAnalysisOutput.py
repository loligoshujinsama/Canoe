import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
import openpyxl


# PseudoCode1
# 1. Read in data from excel
# 2. Save the data from excel into a dictionary
# 3. Convert that dictionary into a wordcloud
# 4. Save that wordcloud as a png.


# PseudoCode2
# 1. Read in data from excel
# 2. Obj is to find the hotel with the highest avr rating
# 3. Read in hotel and rating.
# 4. draw out on paper the output.
# 5. Expected output is the best hotel on average, from there proceed to Pseudocode 1 to

# PseudoCode3
# Objective: Generate a wordcloud based on the rating of the hotel
# Read in from excel: hotel_name, hotel_rating
# gen word cloud

# PseudoCode4
# Objective: Read in Excel, gen word cloud for positive
# Get a list of all reviews based on variable airline(can hardcode for now)
# get a list of every word in the reviews possible as long as they are positive (recommended yes)
# output to word cloud (figure out specifics of how to remove later)

# PS4
def AirLineReview():
    ListForWordCloudOutput = []
    df = pd.read_csv("AirlineReviews.csv", index_col=0)
    df2 = pd.read_excel("ListOfBanned.xlsx", index_col=0)
    DicOfBannedWordsLOL = {}
    DicOfBannedWordsLOL = df2.to_dict()
    ListOfBannedWordsLOL = []
    ListOfBannedWordsLOL = DicOfBannedWordsLOL.get("word_banned")
    ListOfBannedWordsLOL = [value3 for value3 in ListOfBannedWordsLOL.values()]
    print(ListOfBannedWordsLOL)
    ReviewDic = {}
    ReviewDic = df.to_dict()
    ListOfAllReviews = []
    ListOfAllReviews = ReviewDic.get("Review")
    ListOfAllReviews = [value for value in ListOfAllReviews.values()]
    ListOfRating = []
    ListOfRating = ReviewDic.get("Recommended")
    ListOfRating = [value2 for value2 in ListOfRating.values()]
    ListOfPostiveReview = []
    ListOfAirlineName = []
    ListOfAirlineName = ReviewDic.get("AirlineName")
    ListOfAirlineName = [value3 for value3 in ListOfAirlineName.values()]

    for eachrating in range(len(ListOfRating)):

        if ListOfRating[eachrating] == "yes" and ListOfAirlineName[eachrating] == "Wizz Air":
            print(str(eachrating) + " " + ListOfRating[eachrating])
            ListOfPostiveReview.append(ListOfAllReviews[eachrating])

    # Clean the Data
    listSentGoodRev = []
    for eachsent in ListOfPostiveReview:
        splitted = str(eachsent).split(" ")
        for splitter in splitted:
            banthis = False
            if len(splitter) > 3:

                for eachban in ListOfBannedWordsLOL:
                    splitter = splitter.lower()
                    if splitter == eachban:
                        #It is a banned word dun append
                        banthis = True
                if banthis is False:
                    listSentGoodRev.append(str(splitter))

    wordfreqcheck = {}
    for owrd in listSentGoodRev:
        if owrd in wordfreqcheck:
            wordfreqcheck[owrd] += 1
        else:
            wordfreqcheck[owrd] = 1

    return wordfreqcheck


# PS3
def WCHotelRating():
    df = pd.read_excel("hotel.xlsx", index_col=0)
    WCDic = {}
    WCDic = df.to_dict()
    ListOfHotels = []
    ListOfHotels = WCDic.get("hotel_name")
    ListOfHotels = [value for value in ListOfHotels.values()]
    ListOfHotelRatings = []
    ListOfHotelRatings = WCDic.get("hotel_rating")
    ListOfHotelRatings = [value for value in ListOfHotelRatings.values()]

    # Edit out bad records

    ListOfHotelsCLEANED = []
    ListOfHotelRatingsCLEANED = []
    for eachhotel in range(len(ListOfHotels)):
        if ListOfHotelRatings[eachhotel] != "No ratings found":
            ListOfHotelsCLEANED.append(ListOfHotels[eachhotel])
            ListOfHotelRatingsCLEANED.append(float(ListOfHotelRatings[eachhotel]))

    # Combine both list into dic
    mydic = dict(zip(ListOfHotelsCLEANED, ListOfHotelRatingsCLEANED))

    """
    DicOfHotels = {}
    count = 0
    for Hotel in ListOfHotels:
        if ListOfHotelRatings[count] == "No ratings found":
            count += 1
        else:
            print(Hotel, ListOfHotels[count])
            DicOfHotels[Hotel] = ListOfHotels[count]
            DicOfHotels[Hotel][Hotel] = ListOfHotelRatings[count]
            count += 1
    """
    wordcloud3 = generate_word_cloud(mydic)
    wordcloud3.to_file("CLOUDHotelBasedOnRating.png")


# Define a function to recommend hotel by rating
def recommendedhotel():
    ListOfHotelNames = []
    ListOfHotelNamesRemovedDupe = []
    ListOfHotelRating = []
    ListOfHotelPrice = []
    ListOfHotelNames = testdic.get("Hotel")
    ListOfHotelRating = testdic.get("Rating")
    ListOfHotelPrice = testdic.get("Price")
    ListOfHotelNamesRemovedDupe = [name for name in ListOfHotelNames not in ListOfHotelNamesRemovedDupe]
    ListOfAverageRatings = []
    for each in ListOfHotelNamesRemovedDupe:
        currentRange = 0
        CountForLoop = 0
        AcceptedRating = 0
        TotalToAvg = 0
        for eachhotel in range(len(ListOfHotelNames) + 1):

            if eachhotel == each:
                # add the rating to this new list for calculating avg.
                TotalToAvg = TotalToAvg + int(ListOfHotelRating[CountForLoop])
                AcceptedRating = AcceptedRating + 1
            CountForLoop = CountForLoop + 1
        AverageOfRatingCalc = TotalToAvg / AcceptedRating
        ListOfAverageRatings = ListOfAverageRatings.append(AverageOfRatingCalc)

    ComparerCounter = 0
    IndexToTake = 0
    Compared = 0
    for rate in range(len(ListOfAverageRatings) + 1):
        Comparer = int(rate)
        ComparerCounter = ComparerCounter + 1
        if Comparer > Compared:
            Compared = Comparer
            IndexToTake = ComparerCounter
    RecommendedHotelByRating = ListOfHotelNamesRemovedDupe[IndexToTake]
    return RecommendedHotelByRating


# Define a function to generate a word cloud
def generate_word_cloud(words):
    # Create a WordCloud object
    wordcloud = WordCloud(max_font_size=75)

    # Generate the word cloud from the list of words
    wordcloud.generate_from_frequencies(words)

    # Return the word cloud object
    return wordcloud


def read_in_excel_to_dic_for_wordcloud():
    df = pd.read_excel("helloabc.xlsx", index_col=0)
    TheDic = df.to_dict()
    return TheDic


# START OF CODE
WCHotelRating()
airdic = {}
airdic = AirLineReview()
testdic = {}
testdic = read_in_excel_to_dic_for_wordcloud()
DicRating = []
DicReview = []
DicRating = testdic.get('Rating')
DicReview = testdic.get('Review')

listBadReview = []
listGoodReview = []
for each in DicRating:
    if int(each) < 3:
        # bad review
        listBadReview.append(DicReview[each])
    else:
        # good review
        listGoodReview.append(DicReview[each])

# Change list of sentences into list of words
listBadReviewWord = []
for sentence in listBadReview:
    Things = sentence.split(" ")
    for thing in Things:
        if len(thing) > 1:
            listBadReviewWord.append(thing)

listGoodReviewWord = []
for sent in listGoodReview:
    Thongs = sent.split(" ")
    for thong in Thongs:
        if len(thong) > 1:
            listGoodReviewWord.append(thong)

# Get the list of words
# words = ["hello", "hello", "hello", "hello", "machine", "learning", "machine", "xd", "xd", "hello"]
words = []

# Convert the list of words to a dictionary
word_frequencies_bad = {}
word_frequencies_good = {}
for word in listBadReviewWord:
    if word in word_frequencies_bad:
        word_frequencies_bad[word] += 1
    else:
        word_frequencies_bad[word] = 1

for wrod in listGoodReviewWord:
    if wrod in word_frequencies_good:
        word_frequencies_good[wrod] += 1
    else:
        word_frequencies_good[wrod] = 1

# Generate the word cloud
wordcloud = generate_word_cloud(word_frequencies_bad)
wordcloud2 = generate_word_cloud(word_frequencies_good)
wordcloud3 = generate_word_cloud(airdic)
# Save the wordcloud into a png file
wordcloud.to_file("CLOUDNegative.png")
wordcloud2.to_file("CLOUDPositive.png")
wordcloud3.to_file("TESTERPLSWORK.png")

"""
# Display the word cloud (Maybe Testing only)
plt.figure(figsize=(10, 10))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
"""

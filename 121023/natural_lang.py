from airline_review import *
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os
from pathlib import Path
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
EMOTION_TXT = CURRENT_PATH + r'\emotion.txt'

'''
    Downloadables for VADER:
    nltk.download('vader_lexicon')
    nltk.download('punkt')
    nltk.download('stopwords')
'''


def pad_list(dictionary):
    '''
    This function pads the dictionary in the case of uneven array lengths.
    This is required to gracefully convert to dataframe as some airlines 
    may not have equal number of reviews.
    '''
    maxNo = []
    for i in dictionary:
        maxNo.append(len(dictionary[i]))
    for key, value in dictionary.items():
        if len(value) < max(maxNo):
            for i in range(len(value), max(maxNo)):
                dictionary[key].append(None)
    return dictionary


def sentiment_clean_text(text):
    '''
    This function lower all cases and removes punctuations.
    '''
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text


def emotion_tokenise(text):
    '''
    This function tokenises the words and removes stopwords.
    '''
    text = word_tokenize(text, "english")
    stop_words = stopwords.words('english')
    text_list = []

    for word in text:
        if word not in stop_words:
            text_list.append(word)
    return text_list


def emotion_sanitize(file, emotion_dict):
    '''
    This function further sanitizes the emotion dictionary, 
    to remove breaks, commas and apostrophes.
    Returns sanitized emotion dictionary.
    '''
    for line in file:
        clear_line = line.replace("\n", '').replace(",", '').replace("'", '').strip()
        word, emotion = clear_line.split(':')
        emotion_dict[word] = emotion

    return emotion_dict


def sentiment_analyze(text):
    '''
    This function utilizes VADER's SentimentIntensityAnalyzer() to 
    determine polarity scores (negative or positive)
    '''

    # return dictionary of scores
    scores = SentimentIntensityAnalyzer().polarity_scores(text)  
    if (scores['neg'] > scores['pos']):
        return 0
    else:
        return 1


def initiateNLP(dict, airline_name):
    '''
    This function initiates the NLP to process the dictionary passed from 
    the initial flight scraping. Airline name is retrieved from fetchAirlineReview
    as argument for the function.
    '''
    df = pda.DataFrame(pad_list(fetchAirlineReview(dict)[0]))
    emotion_dict = {}

    # get the emotion dictionary ready
    emotion_file = open(EMOTION_TXT, 'r', encoding='utf-8')
    emotion_dict = emotion_sanitize(emotion_file, emotion_dict)
    emotion_file.close()

    # for airline_name in unique_airlines:
    cleaned_text = ""
    temp_emotion_list = []
    words_score_dict = {}
    score = 0
    moods_list = []
    print(f"Working on {airline_name} ...")
    try:
        path = f'static/{airline_name}.png'
        if os.path.exists(path):
            print("OK")
            pass
        else:
            for i in range(len(df[airline_name])):
                # get the review of index i
                text = str(df[airline_name][i])

                # step 1: clean the text
                cleaned_text = sentiment_clean_text(text)

                # Step 2: sentiment Analysis
                score = sentiment_analyze(cleaned_text)
                moods_list.append(score)

                # Step 3: advanced clean for emotions
                cleaned_text_list = emotion_tokenise(cleaned_text)
                df[airline_name][i] = cleaned_text_list

                # Step 4: emotion list builder
                for word in emotion_dict.keys():
                    if word in cleaned_text_list:
                        temp_emotion_list.append(emotion_dict[word])

            words_score_dict = Counter(temp_emotion_list)
            big_emotions = list((key, value) for (key, value) in words_score_dict.items())
            mood = []
            count = []
            for key, value in big_emotions:
                mood.append(key)
                count.append(value)

            # Plotting
            wordcloud = WordCloud(background_color='black', width=800, height=500, random_state=21,
                                  max_font_size=110).generate_from_frequencies(words_score_dict)
            plt.figure(figsize=(10, 7))
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis('off')
            plt.savefig(f'static/{airline_name}.png', dpi=300, bbox_inches='tight')
            print(f"{airline_name}.png created")
    except Exception:
        print(f"{airline_name} has no existing reviews")
        pass


if __name__ == "__main__":
    initiateNLP(dict)

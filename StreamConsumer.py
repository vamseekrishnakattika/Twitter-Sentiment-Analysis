from kafka import KafkaConsumer

import json
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
import nltk
nltk.downloader.download('vader_lexicon')



def main():
    '''
    Consumer consumes tweets from producer
    '''
    # set-up a Kafka consumer
    consumer = KafkaConsumer('twitter')
    for msg in consumer:
        tweet = json.loads(msg.value)
        #print(tweet)
        #print('\n')
        str = get_tweet_sentiment_textblob(tweet.get('text'))
        tweet['sentiment using textblob'] = str
        str = get_tweet_sentiment_nltk(tweet.get('text'))
        tweet['sentiment using nltk'] = str
        print(tweet)
        print('\n')

def clean_tweet(tweet):

    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) (\w+:\ / \ / \S+)", " ", tweet).split())

def get_tweet_sentiment_textblob(tweet):

    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    # Get sentiment
    if analysis.sentiment.polarity > 0:
        return 'This tweet has positive sentiment'
    elif analysis.sentiment.polarity == 0:
        return 'This tweet has neutral sentiment'
    else:
        return 'This tweet has negative sentiment'

def get_tweet_sentiment_nltk(tweet):
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(clean_tweet(tweet))['compound']

    # set sentiment
    if score > 0:
        return 'This tweet has positive sentiment'
    elif score == 0:
        return 'This tweet has neutral sentiment'
    else:
        return 'This tweet has negative sentiment'


if __name__ == "__main__":
    main()

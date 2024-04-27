'''import tweepy
from textblob import  TextBlob
import json

consumer_key= "JdgvD7Ru1NNB7Zt6FxjEDjSaX"
consumer_secret= "uggK0LSIp9e55FFFVs7pEV7QErY61UhOwDp2cAFL6fUEaAopOy"

access_token="1784066254212321280-BIC8sDO9v5JWZLB7yxtqm1SQ5llRyi"
access_token_secret="Av1Knp7M2FVIWF6vJvLpoPQYlmzTQjV7iMlbCa3fPG3XH"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


class StdOutListener(tweepy.StreamListener):
    counter = 0

    def on_data(self, data):
        tweet = json.loads(data)
        analysis = TextBlob(tweet['text'])
        print(tweet['text'])
        print(analysis.sentiment)
        print('-------------------------------------------------------------')
        return True

    def on_error(self, status):
        print(status)

    def on_status(self, status):
        global counter
        counter = counter + 1
        if counter < 5:
            return True
        else:
            return False

myStream = tweepy.Stream(auth = api.auth, listener = StdOutListener())
myStream.filter(track = ["Trump"], languages=["en"])


public_tweets = api.search('Trump')

for tweet in public_tweets:
    print(tweet.text)
    analysis = TextBlob(tweet.text)
    print(analysis.sentiment)
    print('-------------------------------------------------------------')'''

import tweepy
from textblob import TextBlob
import json

consumer_key = "JdgvD7Ru1NNB7Zt6FxjEDjSaX"
consumer_secret = "uggK0LSIp9e55FFFVs7pEV7QErY61UhOwDp2cAFL6fUEaAopOy"
access_token = "1784066254212321280-BIC8sDO9v5JWZLB7yxtqm1SQ5llRyi"
access_token_secret = "Av1Knp7M2FVIWF6vJvLpoPQYlmzTQjV7iMlbCa3fPG3XH"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


class StdOutListener(tweepy.StreamListener):
    counter = 0

    def on_data(self, data):
        tweet = json.loads(data)
        analysis = TextBlob(tweet['text'])
        print(tweet['text'])
        print(analysis.sentiment)
        print('-------------------------------------------------------------')
        self.counter += 1
        if self.counter >= 5:  # Limit to 5 tweets for demonstration
            return False
        return True

    def on_error(self, status):
        print(status)


myStreamListener = StdOutListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(track=["Trump"], languages=["en"])


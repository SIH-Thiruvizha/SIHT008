import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from textblob import TextBlob
import matplotlib.pyplot as plt
import re

def calctime(a):
    return time.time()-a

positive = 0
negative = 0
compound = 0
count = 0

initime = time.time()
plt.ion()

import test

consumerKey = "zKlrJwSDOW5WKpyvrOYpMsxwj"
consumerSecret = "ojx0AWNIFRAMO8nSj1dKlPlfy9XkjRzhDalRCncAbXouRRJOC2"
accessToken = "1676112845828939777-G5W4grFXLJImlkaPaHfrBQdoFPAVmf"
accessTokenSecret = "rarR0OhvSHAznHuNj98fU1m4ix31ygXqeJ3zZCDrVD4kB"

class listner(StreamListener):

    def on_data(self, data):
        global initime
        t = int(calctime(initime))
        all_data = json.loads(data)
        tweet = all_data["text"]#.encode("utf-8")
        tweet = "".join(re.findall("[a-zA-Z]+", tweet))
        blob = TextBlob(tweet.strip())

        global count
        global positive
        global negative
        global compound

        count = count+1
        senti = 0

        for sen in blob.sentences:
            senti = senti + sen.sentiment.polarity

            if sen.sentiment.polarity >= 0:
                positive = positive + sen.sentiment.polarity
            else:
                negative = negative + sen.sentiment.polarity

        compound = compound + senti

        print(count)
        print(tweet.strip())
        print(senti)
        print(t)
        print(str(positive) + " " + str(negative) + " " + str(compound))

        plt.axis([0, 70, -20, 20])
        plt.xlabel('Time')
        plt.ylabel('Sentiment')
        plt.plot([t], [positive], [negative], 'go', [t], [negative], 'ro', [compound], 'bo')
        plt.show()
        plt.pause(0.0001)
        if count == 200:
            return False
        else:
            return True
    def on_error(self, status_code):
        print(status_code)

auth = OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)

twitterStream = Stream(auth, listner(count))
twitterStream.filter(track=["Narendra Modi"])

import re
import json
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from flask import Flask, render_template, request


app = Flask(__name__)


class TwitterClient(object):
	"""
	Generic Twitter Class for sentiment analysis.
	"""

	def __init__(self):
		"""
		Class constructor or initialization method.
		"""
		# keys and tokens from the Twitter Dev Console
		consumer_key = 'JdgvD7Ru1NNB7Zt6FxjEDjSaX'
		consumer_secret = 'uggK0LSIp9e55FFFVs7pEV7QErY61UhOwDp2cAFL6fUEaAopOy'
		access_token = '1784066254212321280-BIC8sDO9v5JWZLB7yxtqm1SQ5llRyi'
		access_token_secret = 'Av1Knp7M2FVIWF6vJvLpoPQYlmzTQjV7iMlbCa3fPG3XH'

		# attempt authentication
		try:
			# create OAuthHandler object
			self.auth = OAuthHandler(consumer_key, consumer_secret)
			# set access token and secret
			self.auth.set_access_token(access_token, access_token_secret)
			# create tweepy API object to fetch tweets
			self.api = tweepy.API(self.auth)
		except:
			print("Error: Authentication Failed")

	def clean_tweet(self, tweet):
		'''
		Utility function to clean tweet text by removing links, special characters
		using simple regex statements.
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

	def get_tweet_sentiment(self, tweet):
		'''
		Utility function to classify sentiment of passed tweet
		using textblob's sentiment method
		'''
		# create TextBlob object of passed tweet text
		analysis = TextBlob(self.clean_tweet(tweet))
		# set sentiment
		if analysis.sentiment.polarity > 0:
			return 'positive'
		elif analysis.sentiment.polarity == 0:
			return 'neutral'
		else:
			return 'negative'

	def get_tweets(self, query, count=10):
		'''
		Main function to fetch tweets and parse them.
		'''
		# empty list to store parsed tweets
		tweets = []

		try:
			# call twitter api to fetch tweets
			fetched_tweets = self.api.search(q=query, count=count)

			# parsing tweets one by one
			for tweet in fetched_tweets:
				# empty dictionary to store required params of a tweet
				parsed_tweet = {}

				# saving text of tweet
				parsed_tweet['text'] = tweet.text
				# saving sentiment of tweet
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

				# appending parsed tweet to tweets list
				if tweet.retweet_count > 0:
					# if tweet has retweets, ensure that it is appended only once
					if parsed_tweet not in tweets:
						tweets.append(parsed_tweet)
				else:
					tweets.append(parsed_tweet)

			# return parsed tweets
			return tweets
			

		except tweepy.TweepError as e:
			# print error (if any)
			print("Error : " + str(e))



"""
	# printing first 5 positive tweets
	print("\n\nPositive tweets:")
	for tweet in ptweets[:10]:
		print(tweet['text'])

	# printing first 5 negative tweets
	print("\n\nNegative tweets:")
	for tweet in ntweets[:10]:
		print(tweet['text'])
"""

"""Api Routes"""
"""def index():
	if request.method == "POST":
		query = request.form['query']
		
		print(query)
		return query
	else:
		data = main()
		return render_template('index.html', data=data)"""
@app.route('/', methods=['GET','POST'])
def main():
	# creating object of TwitterClient Class

	if request.method == "POST":
		query = request.form['query']
		count = request.form['count']

		api = TwitterClient()
		# calling function to get tweets
		tweets = api.get_tweets(query=query, count=count)
		# picking positive tweets from tweets
		ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
		# picking negative tweets from tweets
		ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

		# percentage of positive tweets
		positive = "{0:.2f}".format(100 * len(ptweets) / len(tweets))
		# percentage of negative tweets
		negative = "{0:.2f}".format(100 * len(ntweets) / len(tweets))
		# percentage of neutral tweets
		neutral = "{0:.2f}".format(100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets))
		results = [positive, negative, neutral, query, count]

		print(query)
		return render_template('index.html', data = results)
	else:
		return render_template('index.html')


if __name__ == "__main__":
	# calling main function
	app.run(debug=True,port=5001)

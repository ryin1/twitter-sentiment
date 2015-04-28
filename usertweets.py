from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy

import pickle
import code
import json

CONSUMER_KEY="6iofbm8uS4tzDzvidhh7LqFjy"
CONSUMER_SECRET="3hCbXm9iChIc75SDo9StrRPz3zfPhaqXFwB6BnKHfz1lko2zQD"

ACCESS_TOKEN="2982406223-UTrA8HCfWEEYZwNpAsT6aH0cLwNISzf6mQpSGCT"
ACCESS_TOKEN_SECRET="kO6XPYfajMvWL5luLtPkq75XcNDMFQqdbgvzjSzwccRGO"
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

USER_ID = 'locodoco'
tweets = []
count = 0
for page in tweepy.Cursor(api.user_timeline, id=USER_ID).pages(10):
	for tweet in page:
		print(tweet.text.encode('utf-8'))
		tweets.append(tweet._json)
		count += 1

with open('{}_data.pickle'.format(USER_ID), 'wb') as f:
	pickle.dump(tweets, f)
print('\n\n\nCOUNT = {}'.format(count))

from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from analysis import Analyzer


import tweepy
import pickle
import json
import time
import code
import analysis

CONSUMER_KEY="7ZI3BzYpi1v0ZTJvsbjB696tN"
CONSUMER_SECRET="vzwV9riclXjPYv1TqQUjN9UaoAAiet9EAHqjPYdWIOcQ1DQWYj"

ACCESS_TOKEN="2982406223-rIgKwKlpduITV7hkrreYBkFQDw0AY7wiMDR79pr"
ACCESS_TOKEN_SECRET="T2lzQA9YFWxuHeYmyLM6715iXlXUg8fl8TzWpv9PugRzj"

lim = 30

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    tweets = []
    count = 0
    stop = False

    def close(self):
        self.stop = True

    def on_data(self, data):
        if self.stop:
            print('Stream closed.')
            return False
        self.count += 1
        d = json.loads(data)
        self.tweets.append(d)
        if self.count >= lim:
            with open('tweet_stream.pickle', 'wb') as f:
                pickle.dump(self.tweets, f)
            return False
        return True

    def on_error(self, status):
        print(status)

def gather_tweets(username=None, keyword=None, limit=200):#, duration=10):
    if username:
        tweets = []
        count = 0
        for page in tweepy.Cursor(api.user_timeline, id=username).pages(10):
            for tweet in page:
                print(tweet.text.encode('utf-8'))
                tweets.append(tweet._json)
                count += 1
                if count > limit:
                    break
        return tweets
    elif keyword:
        l = StdOutListener()
        stream = Stream(auth, l)
        global lim
        lim = limit
        stream.filter(track=[keyword])
        with open('tweet_stream.pickle', 'rb') as f:
            return pickle.load(f)
    else:
        raise ValueError('Invalid Arguments. username and keyword both' + 
                         'can\'t be None')

if __name__ == '__main__':
    s = 'baltimore'
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    #tweets = gather_tweets(username=s) # last 200 tweets
    tweets = gather_tweets(keyword=s, limit=100)
    #print('tweets',tweets)
    # Create analyzer
    analyzer = Analyzer(tweets, s)
    avg = analyzer.calc_sentiment()
    #keywrds = analyzer.get_keywords()
    analyzer.save_sentiment_data()

from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import pickle
import json

CONSUMER_KEY="7ZI3BzYpi1v0ZTJvsbjB696tN"
CONSUMER_SECRET="vzwV9riclXjPYv1TqQUjN9UaoAAiet9EAHqjPYdWIOcQ1DQWYj"

ACCESS_TOKEN="2982406223-rIgKwKlpduITV7hkrreYBkFQDw0AY7wiMDR79pr"
ACCESS_TOKEN_SECRET="T2lzQA9YFWxuHeYmyLM6715iXlXUg8fl8TzWpv9PugRzj"

time = 0

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    tweets = []
    count = 0
    
    def on_data(self, data):
        self.count += 1
        print(data)
        d = json.loads(data)
        self.tweets.append(d)
        if self.count >= 30:
            with open('tweet_data.pickle', 'wb') as f:
                pickle.dump(self.tweets, f)
            return False
        return True

    def on_error(self, status):
        print(status)

def gather_tweets(username=None, keyword=None, limit, time):
    if username:
        tweets = []
        count = 0
        for page in tweepy.Cursor(api.user_timeline, id=username).pages(10):
            for tweet in page:
                print(tweet.text.encode('utf-8'))
                tweets.append(tweet._json)
                count += 1
                if count > limit:
                    with open('tweet_data.pickle', 'wb') as f:
                        pickle.dump(tweets, f)
                    return
    else if keyword:
        l = StdOutListener()
        stream = Stream(auth, l)
        stream.filter(track=[keyword])
    else:
        raise ValueError('Invalid Arguments. username and keyword both' + 
                         'can\'t be None')

if __name__ == '__main__':
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    gather_tweets(username='locodoco', )
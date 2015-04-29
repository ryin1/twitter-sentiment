from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import pickle
import json

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="7ZI3BzYpi1v0ZTJvsbjB696tN"
consumer_secret="vzwV9riclXjPYv1TqQUjN9UaoAAiet9EAHqjPYdWIOcQ1DQWYj"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="2982406223-rIgKwKlpduITV7hkrreYBkFQDw0AY7wiMDR79pr"
access_token_secret="T2lzQA9YFWxuHeYmyLM6715iXlXUg8fl8TzWpv9PugRzj"

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    tweets=[]
    def on_data(self, data):
        print(data)
        d = json.loads(data)
        self.tweets.append(d)
        with open('ilovepoop.pickle', 'wb') as f:
            pickle.dump(self.tweets, f)
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['basketball'])
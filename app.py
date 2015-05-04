from __future__ import absolute_import, print_function
from flask import Flask, render_template, request, redirect, url_for, json
import time
import bs4
import tweepy
import requests
import stream
import random

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from analysis import Analyzer
from stream import StdOutListener

# Create app
app = Flask(__name__)
CONSUMER_KEY = "7ZI3BzYpi1v0ZTJvsbjB696tN"
CONSUMER_SECRET = "vzwV9riclXjPYv1TqQUjN9UaoAAiet9EAHqjPYdWIOcQ1DQWYj"

ACCESS_TOKEN = "2982406223-rIgKwKlpduITV7hkrreYBkFQDw0AY7wiMDR79pr"
ACCESS_TOKEN_SECRET = "T2lzQA9YFWxuHeYmyLM6715iXlXUg8fl8TzWpv9PugRzj"


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        # render homepage template
        return render_template('boot.html')
    else:
        # grab POST form data
        data = request.form

        # parse as JSON
        jsondata = json.dumps(data, separators=(',', ':'))
        if 'topic' in jsondata:
            new_data = json.loads(jsondata)
            new_data['rand'] = str(int(random.random() * 999999999))
            print('\n\n\n', int(new_data['limit'][0]), type(
                int(new_data['limit'][0])), '\n\n\n')
            auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
            api = tweepy.API(auth)
            # tweets = gather_tweets(username=s) # Last 50 tweets
            tweets = stream.gather_tweets(
                api, auth, keyword=new_data['topic'][0],
                limit=int(new_data['limit'][0]))
            # Create analyzer
            analyzer = Analyzer(tweets, new_data['topic'][0])
            avg = analyzer.calc_sentiment()
            # keywrds = analyzer.get_keywords()
            analyzer.save_sentiment_data(int(new_data['rand']))
            return redirect((url_for('log', data=json.dumps(new_data),
                                     mode='debug')))
        elif 'username' in jsondata:
            print('\n\n', 'you submitted a username', '\n\n')
            new_data = json.loads(jsondata)
            new_data['rand'] = str(int(random.random() * 999999999))
            auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
            api = tweepy.API(auth)
            # tweets = gather_tweets(username=s) # last 200 tweets
            tweets = stream.gather_tweets(
                api, auth, username=new_data['username'][0], limit=30)
            # print('tweets',tweets)
            # Create analyzer
            analyzer = Analyzer(tweets, new_data['username'][0])
            avg = analyzer.calc_sentiment()
            # keywrds = analyzer.get_keywords()
            analyzer.save_sentiment_data(int(new_data['rand']))
            return redirect((url_for('log', data=json.dumps(new_data),
                                     mode='debug')))


@app.route('/log/<data>/<mode>')
def log(data, mode):
    jsondata = json.loads(data)
    if 'username' in jsondata:
        username = jsondata['username'][0]
        req = requests.get('https://twitter.com/' + username)
        response_text = req.text
        bs = bs4.BeautifulSoup(response_text)
        class_string = ('ProfileAvatar-container u-block js-tooltip '
                        'profile-picture media-thumbnail')
        profile_image_url = bs.find_all(
            class_=class_string, href=True)[0]['href']
        # render homepage template
        return render_template('success.html', username=username,
                               profile_image_url=profile_image_url,
                               rand=jsondata['rand'])
    elif 'topic' in jsondata:
        topic = jsondata['topic'][0]
        limit = int(jsondata['limit'][0])
        # render homepage template
        return render_template('stream.html', topic=topic, limit=limit,
                               rand=jsondata['rand'])
    else:
        # render homepage template
        return render_template('boot.html')


def main():
    global analysis_data
    analysis_data = dict()
    app.debug = True
    app.config["CACHE_TYPE"] = "null"
    app.run()


if __name__ == "__main__":
    main()

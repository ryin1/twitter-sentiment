from __future__ import absolute_import, print_function
from flask import Flask, render_template, request, redirect, url_for, json
import time
import bs4
import tweepy
import requests
import stream


from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from analysis import Analyzer
from stream import StdOutListener

# Create app
app = Flask(__name__)
CONSUMER_KEY="7ZI3BzYpi1v0ZTJvsbjB696tN"
CONSUMER_SECRET="vzwV9riclXjPYv1TqQUjN9UaoAAiet9EAHqjPYdWIOcQ1DQWYj"

ACCESS_TOKEN="2982406223-rIgKwKlpduITV7hkrreYBkFQDw0AY7wiMDR79pr"
ACCESS_TOKEN_SECRET="T2lzQA9YFWxuHeYmyLM6715iXlXUg8fl8TzWpv9PugRzj"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        # render homepage template
        return render_template('boot.html')
    else:
        # grab POST form data
        data = request.form

        # parse as json
        jsondata = json.dumps(data, separators=(',', ':'))
        if 'topic' in jsondata:
            new_data = json.loads(jsondata)
            auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
            api = tweepy.API(auth)
            # tweets = gather_tweets(username=s) # last 200 tweets
            tweets = stream.gather_tweets(api, auth, keyword=new_data['topic'][0], limit=time)
            # print('tweets',tweets)
            # Create analyzer
            analyzer = Analyzer(tweets, new_data['topic'][0])
            avg = analyzer.calc_sentiment()
            # keywrds = analyzer.get_keywords()
            analyzer.save_sentiment_data()
            return redirect((url_for('log', data=jsondata, mode='debug')))
        elif 'username' in jsondata:
            print('\n\n', 'you submitted a username', '\n\n')
            new_data = json.loads(jsondata)
            auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
            api = tweepy.API(auth)
            # tweets = gather_tweets(username=s) # last 200 tweets
            tweets = stream.gather_tweets(api, auth, username=new_data['username'][0])
            # print('tweets',tweets)
            # Create analyzer
            analyzer = Analyzer(tweets, new_data['username'][0])
            avg = analyzer.calc_sentiment()
            # keywrds = analyzer.get_keywords()
            analyzer.save_sentiment_data()
            return redirect((url_for('log', data=jsondata, mode='debug')))


@app.route('/log/<data>/<mode>')
def log(data, mode):
    jsondata = json.loads(data)
    if 'username' in jsondata:
        username = jsondata['username'][0]
        req = requests.get('https://twitter.com/' + username)
        response_text = req.text
        bs = bs4.BeautifulSoup(response_text)
        profile_image_url = bs.find_all(class_='ProfileAvatar-container u-block js-tooltip profile-picture media-thumbnail', href=True)[0]['href']
        # render homepage template
        return render_template('success.html', username=username, profile_image_url=profile_image_url)
    elif 'topic' in jsondata:
        topic = jsondata['topic'][0]
        # render homepage template
        return render_template('stream.html', topic=topic, data=jsondata)
    else:
        # render homepage template
        return render_template('boot.html')


def main():
    global poop
    global analysis_data
    poop = False
    analysis_data = dict()
    app.debug = True
    app.run()


if __name__ == "__main__":
    main()

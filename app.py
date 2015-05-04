from __future__ import absolute_import, print_function
from flask import Flask, render_template, request, redirect, url_for, json
from tweepy import OAuthHandler
from analysis import Analyzer
import bs4
import tweepy
import requests
import stream
import random

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
            # load data into dictionary
            new_data = json.loads(jsondata)

            # create random number for this graph
            new_data['rand'] = str(int(random.random() * 999999999))

            # connect to twitter
            auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
            api = tweepy.API(auth)

            # get the tweets
            tweets = stream.gather_tweets(
                api, auth, keyword=new_data['topic'][0],
                limit=int(new_data['limit'][0]))

            # Create analyzer
            analyzer = Analyzer(tweets, new_data['topic'][0])
            analyzer.save_sentiment_data(int(new_data['rand']))

            # render results page
            return redirect((url_for('log', data=json.dumps(new_data),
                                     mode='debug')))
        elif 'username' in jsondata:
            # load data into dictionary
            new_data = json.loads(jsondata)

            # create random number for this graph
            new_data['rand'] = str(int(random.random() * 999999999))

            # connect to twitter
            auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
            api = tweepy.API(auth)

            # get the tweets
            tweets = stream.gather_tweets(
                api, auth, username=new_data['username'][0], limit=50)

            # Create analyzer
            analyzer = Analyzer(tweets, new_data['username'][0])

            analyzer.save_sentiment_data(int(new_data['rand']))
            return redirect((url_for('log', data=json.dumps(new_data),
                                     mode='debug')))


@app.route('/log/<data>/<mode>')
def log(data, mode):
    jsondata = json.loads(data)
    if 'topic' in jsondata:
        # load variables that will be displayed on the page
        topic = jsondata['topic'][0]
        limit = int(jsondata['limit'][0])

        # render streaming template
        return render_template('stream.html', topic=topic, limit=limit,
                               rand=jsondata['rand'])
    elif 'username' in jsondata:
        # load username that will be displayed on the page
        username = jsondata['username'][0]

        # get the url for the profile picture of the username
        req = requests.get('https://twitter.com/' + username)
        response_text = req.text
        bs = bs4.BeautifulSoup(response_text)
        class_string = ('ProfileAvatar-container u-block js-tooltip '
                        'profile-picture media-thumbnail')
        profile_image_url = bs.find_all(
            class_=class_string, href=True)[0]['href']

        # render username query success template
        return render_template('success.html', username=username,
                               profile_image_url=profile_image_url,
                               rand=jsondata['rand'])
    else:
        # render homepage template
        return render_template('boot.html')


def main():
    app.debug = True
    app.run()


if __name__ == "__main__":
    main()

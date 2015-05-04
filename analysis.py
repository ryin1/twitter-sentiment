from datetime import datetime
from graph import Plotter
from alchemyapi import AlchemyAPI

import code
import pickle
import time


# Function timer decorator
def timeit(function):
    def timed(*args, **kwargs):
        start = time.time()
        result = function(*args, **kwargs)
        end = time.time()
        runtime = end - start
        print('{}: FINISHED in {} sec ({} minutes)'.format(function.__name__,
                                                           runtime,
                                                           runtime / 60))
        return result
    return timed


# Helper to convert date string into datetime
def datetime_of_tweet(tweet):
    s = tweet['created_at']
    datestr = s[4:19] + s[-5:]
    return datetime.strptime(datestr, '%b %d %H:%M:%S %Y')


class Analyzer():

    def __init__(self, tweets, descrip):
        self.tweets = tweets
        self.alchemy = AlchemyAPI()
        self.keywords = {}
        self.keyword_list = []
        self.descrip = descrip

    @timeit
    def calc_sentiment(self):
        ''' Returns average sentiment of all the Analyzer's tweets. '''
        score = 0
        for tweet in self.tweets:
            sentiment = self.alchemy.sentiment('text', tweet['text'])
            #if sentiment['status'] != 'OK':
            #    raise Exception('AlchemyAPI daily transaction limit exceeded.'
            #                    ' Change API Key.')
            if 'docSentiment' not in sentiment:
                # We ignore these "Errors" in our analysis.
                continue
            sentiment = sentiment['docSentiment']
            if sentiment['type'] != 'neutral':
                score += float(sentiment['score'])
                tweet['sentiment'] = float(sentiment['score'])
            else:
                tweet['sentiment'] = 0.0
        return score / len(self.tweets)

    def save_sentiment_data(self, num):
        ''' Pickle-dumps tweet sentiment for a given input against time. '''
        times, sents = [], []
        for tweet in self.tweets:
            if 'sentiment' in tweet:
                times.append(datetime_of_tweet(tweet))
                sents.append(tweet['sentiment'])
            else:
                pass
        plotter = Plotter(times, sents, self.descrip)
        plotter.save_graph(num)

    @timeit
    def get_keywords(self):
        ''' Returns top keywords in the tweets. '''
        for tweet in self.tweets:
            tweet_words = self.alchemy.keywords('text', tweet['text'])
            if 'keywords' not in tweet_words:
                continue
            tweet_words = tweet_words['keywords']
            tweet['keywords'] = tweet_words
            for word in tweet_words:
                word_text = word['text']
                if word_text not in self.keywords:
                    self.keywords[word_text] = float(word['relevance'])
                else:
                    self.keywords[word_text] += float(word['relevance'])
        max_relev = max(self.keywords.values())
        for k, v in self.keywords.items():
            self.keywords[k] /= max_relev
        self.keyword_list = sorted(self.keywords.items(), key=lambda x: x[1],
                                   reverse=True)
        return self.keyword_list

if __name__ == '__main__':
    PICKLE_NAME = 'stream_data.pickle'
    with open('locodoco_data.pickle', 'rb') as f:
        tweets = pickle.load(f)
    analyzer = Analyzer(tweets, 'locodoco')
    avg = analyzer.calc_sentiment()
    keywrds = analyzer.get_keywords()
    analyzer.save_sentiment_data()

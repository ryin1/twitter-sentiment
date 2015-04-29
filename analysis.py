import pickle
from alchemyapi import AlchemyAPI
alchemyapi = AlchemyAPI()
import code
from datetime import datetime
from graph import Plotter

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

    def calc_sentiment(self):
        ''' Returns average sentiment of all the Analyzer's tweets. '''
        score = 0
        for tweet in self.tweets:
            sentiment = self.alchemy.sentiment('text', tweet['text'])
            if 'docSentiment' not in sentiment:
                # We ignore these "Errors" in our analysis.
                #print('calcing sentiment didnt find sentiment in {}'.format(tweet['text'].encode('utf-8')))
                continue
            sentiment = sentiment['docSentiment']
            if sentiment['type'] != 'neutral':
                score += float(sentiment['score'])
                tweet['sentiment'] = float(sentiment['score'])
            else:
                tweet['sentiment'] = 0.0
        return score / len(self.tweets)

    def save_sentiment_data(self):
        ''' Pickle-dumps tweet sentiment for a given input against time. '''
        # with open('graph_data.pickle', 'wb') as f:
        times, sents = [], []
        for tweet in self.tweets:
            if 'sentiment' in tweet:
                #print('found a sentiment')
                times.append(datetime_of_tweet(tweet))
                sents.append(tweet['sentiment'])
            else:
            	pass
                #print('didnt find  a sentiment in: {}'.format(tweet['text'].encode('utf-8')))
        plotter = Plotter(times, sents, self.descrip)
        plotter.save_graph()
        plotter.open_graph()

    def get_keywords(self):
        ''' Returns top keywords in the tweets. '''
        for tweet in self.tweets:
            tweet_words = self.alchemy.keywords('text', tweet['text'])
            if 'keywords' not in tweet_words:
                continue
            tweet_words = tweet_words['keywords']
            tweet['keywords'] = tweet_words
            for word in tweet_words:
                word_text = word['text'].encode('utf-8')
                if word_text not in self.keywords:
                    self.keywords[word_text] = float(word['relevance'])
                else:
                    self.keywords[word_text] += float(word['relevance'])
        max_relev = max(self.keywords.values())
        # print(max_relev)
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

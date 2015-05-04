import plotly.plotly as py
import pickle
import os
import code
import time

from plotly.graph_objs import *
from datetime import datetime


def timeit(function):
    def timed(*args, **kwargs):
        start = time.time()
        result = function(*args, **kwargs)
        end = time.time()
        runtime = end - start

        print('{}: FINISHED in {} sec ({} min)'.format(function.__name__,
                                                       runtime, runtime / 60))
        return result
    return timed


class Plotter():

    @timeit
    def __init__(self, x, y, desc):
        self.x = x
        self.y = y
        self.desc = desc
        py.sign_in("ryin", "dyg27kojki")
        self.layout = Layout(title='{}\'s Sentiment Graph'.format(desc),
                             xaxis=XAxis(
            title='Date and Time',
            font=Font(
                family='Courier New, monospace',
                size=16,
                color='#7f7f7f'
            )
        ),
            yaxis=YAxis(
            title='Sentiment Score',
            font=Font(
                family='Courier New, monospace',
                size=16,
                color='#7f7f7f'
            )
        )
        )
        self.data = Data([Scatter(x=x, y=y, mode="lines+markers")])

    def __str__(self):
        return 'X values: {}\nY values: {}'.format(x, y)

    def save_graph(self, num):
        if os.path.isfile('static/img/{}.png'.format(self.desc)):
            os.remove('static/img/{}.png'.format(self.desc))
        py.image.save_as({'data': self.data, 'layout': self.layout},
                         'static/img/{}_{}.png'.format(self.desc, num))

    def open_graph(self):
        plot_url = py.plot(self.data, layout=self.layout,
                           filename='Tweet Sentiment for {}'.format(self.desc))
        return plot_url

if __name__ == '__main__':
    with open('graph_data.pickle', 'rb') as f:
        x, y = pickle.load(f)

    plotter = Plotter(x, y, '@locodoco')
    print(plotter)
    plotter.save_graph()
    plotter.open_graph()

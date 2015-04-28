import plotly.plotly as py
from plotly.graph_objs import *
import pickle
from datetime import datetime

class Plotter():

	def __init__(self, x, y, username):
		self.x = x
		self.y = y
		self.username = username
		py.sign_in("ryin", "dyg27kojki")
		self.layout = Layout(title='{}\'s Sentiment Graph'.format(username),
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
		self.data = Data([Scatter(x=x, y=y)])
	def save_graph(self):
		py.image.save_as({'data': self.data, 'layout': self.layout},
						'{}_graph.png'.format(self.username))
	def open_graph(self):
		plot_url = py.plot(self.data, layout=self.layout,
							filename='{}\'s Tweet Sentiment'.format(self.username))
		return plot_url

with open('graph_data.pickle', 'rb') as f:
	x,y = pickle.load(f)

plotter = Plotter(x,y, '@locodoco')
plotter.save_graph()
plotter.open_graph()
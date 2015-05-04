Group members: Raymond Yin

Brief Description of Project Goals/Features:
Twitter Sentiment Analysis is deployed as a webapp on Flask, and has two options:
1. Given a Twitter username and an integer limit, our app takes the last tweets up to the limit of the username and graphs the sentiment score [-1, 1] of each tweet vs. time, displaying it on the page along with the Twitter user’s profile picture.
2. Given a keyword query and an integer limit, our app checks the dynamically changing Twitter stream for tweets related to the keyword up to the limit and graphs the sentiment score [-1, 1] of each tweet vs. time.

Instructions to run:
Before running, make sure dependencies are met (see requirements.txt).
> python3 app.py
> Choose one of the two fields and follow the instructions on the page.

*** IMPORTANT *** If graphs are empty, it is very likely that the api_key exceeded the daily API limit. To fix, change api_key.txt’s contents to a different Alchemy API key in other_keys.txt.

Requirements Met:
  Custom class:
Plotter (graph.py) has __str__ magic method.
Analyzer (analysis.py)

Both classes use the timeit decorator.

  Three Modules:
    1 -> flask
    2 -> pickle
    3 -> os

   Custom Decorator or Generator function:
   timeit decorator, used in both analysis.py and graph.py

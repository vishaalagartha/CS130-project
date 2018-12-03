# CS130 Project - RedditCloud Application
This repository contains the backend for the RedditCloud application.

### Requirements
  - Python 3.6 (https://www.python.org/downloads/)
  - Python requests module (http://docs.python-requests.org/en/master/)
  - Natural Language Toolkit (NLTK) (https://www.nltk.org/)
    - Once downloaded, open Python interpreter and run `python -m nltk.downloader all`
  - vaderSentiment (https://github.com/cjhutto/vaderSentiment)

### Directory structure
  - DataCrawler - contains DataCrawler module with the following files
     - `server.py` - Python server to handle requests
     - `data_crawler.py` - Reddit crawler
     - `test_data_crawler.py` - Unittests for DataCrawler and end-to-end tests for backend 
  - SentimentModel - contains SentimentModel module with the following main files
     - `sentiment_model.py` - Main file to handle comments and generate sentiments
     - `test_sentiment_model.py` - Unittests for SentimentModel
     - `svo.py` - Separates comments into Subject, Verb, Object format
  - `index.html` - Entry file for documentation
  - docs - contains all documentation for frontend and backend application


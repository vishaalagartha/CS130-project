# CS130-project

In Part B, our team is working on modules on 3 separate branches:
  - master: The master branch contains the working code for the SentimentModel and the DataCrawler modules
  - sentiment-analysis: This branch contains the working code for the SentimentModel. Since it was branched from master, it also contains the DataCrawler module.
  - sent_chart: This branch contains the working code for the SentimentChart module. Since it was branched from master, it also contains the DataCrawler module.

DataCrawler Module
  - server.py: the RequestHandler class
  - data_crawler.py: the DataCrawler class
  - constants.py: COMMON_WORDS (not currently implemented) and default endpoints
  - test.py: all unittest cases

Sentiment Analysis Module
  - negative-words.csv: List of 4000+ negative sentiment words
  - positive-words.csv: List of 2000+ positive sentiment words
  - sentiment_model: SentimentModel class currently using an external API for sentiment analysis
  - words.py: load csv files into lists

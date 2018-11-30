"""
The SentimentModel class can be used to generate sentiments based on an input of comments
and their respective votes from a specific subreddit between two timestamps.
"""
# https://github.com/cjhutto/vaderSentiment#python-code-example
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

class SentimentModel:
    """
    Encapsulates an instance of the Sentiment class and its methods
    """
    def __init__(self, comments):
        """
        Construct a new instance of a SentimentModel, initialize the SentimentIntensityModel
        Calls handleComments() to split comments into phrases

        :param comments: List of dictionaries containing 'comment','votes' and 'timestamps'
        fields; 'comment' is a string and 'votes' and 'timestamps' are integers

        :return None
        """
        self.comments_ = self.handleComments(comments)
        self.model_ = SentimentIntensityAnalyzer()

    def handleComments(self, comments):
        """
        Split comments into simple phrases using a Subject-Verb-Object model
        generated from Stanford Parser

        :param comments: List of dictionaries containing 'comment','votes' and 'timestamps'
        fields; 'comment' is a string and 'votes' and 'timestamps' are integers
        
        :return phrases: List of dictionaries containing 'phrase','votes' and 'timestamps'
        fields; 'phrase' is a string and 'votes' and 'timestamps' are integers
        """
        # Grab comments that have specific word
        # Parse through comments using Subject-Predicate-Object and split comment into phrases
        phrases = []    # list of dicts: 'phrase', 'vote'

        for comment in comments:
            #list of lists 0 is comment 1 is vote
            sentence = comment[0].split(".")
            vote = comment[1]
            timestamp = comment[2]
            for i in sentence:
                phrase = re.split('; |, | and | but | or | nor ', i)
            # phrases.append([word for word in phrase])

                # If we have the timestamps for each comment/post, we can store it here
                for j in phrase:
                    phrases.append({'phrase': j, 'vote': vote, 'timestamp': timestamp})
        return phrases  

    def generateSentiments(self, word):
        """
        Generate sentiment given a specific word. Searches for the word in list of phrases
        and generates a sentiment for the specific word.

        :param word: String selected by user on front end, sent to SentimentModel to
        generate sentiment of subreddit with the respect to selected word
        
        :return phrases: List of dictionaries containing 'phrase','votes' and 'timestamps'
        fields; 'phrase' is a string and 'votes' and 'timestamps' are integers
        """
        # Run it through the SentimentIntensityAnalyzer
        related_phrases = []
        for d in self.comments_:
            if word.lower() in d['phrase'].lower():
                related_phrases.append(d)

        sentiment_values = []
        avg = 0
        for i in related_phrases:
            vs = self.model_.polarity_scores(i['phrase'])
            sentiment_values.append({'score': vs, 'vote': vote, 'timestamp': timestamp})
            
            # sentiment_values.append(vs)
            # print("{:-<65} {}".format(i['phrase'], str(vs['compound']*i['vote'])))
            #avg += vs['compound']*i['vote']

        # Need to normalize score once we factor in upvotes
#         if related_phrases:
#             score = avg / len(related_phrases)
#             if score >= 0.05:
#                 print('Positive')
#             elif score <= -0.05:
#                 print('MEGATIVE')
#             else:
#                 print('Neutral')

        return sentiment_values

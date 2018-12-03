"""
The SentimentModel class can be used to generate sentiments based on an input of comments
and their respective votes from a specific subreddit between two timestamps.
"""
# https://github.com/cjhutto/vaderSentiment#python-code-example
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from svo import SVO
import re

class SentimentModel:
    """
    Encapsulates an instance of the Sentiment class and its methods
    """
    def __init__(self, comments):
        """
        Construct a new instance of a SentimentModel, initialize the SentimentIntensityModel
        Calls handleComments() to split comments into phrases

        :param comments: List of dictionaries containing 'comment', 'vote', and 'timestamp'
        fields; 'comment' is a string and 'vote' and 'timestamp' are integers

        :return None
        """
        self.comments_ = self.handleComments(comments)
        self.model_ = SentimentIntensityAnalyzer()

    def handleComments(self, comments):
        """
        Split comments into simple phrases using a Subject-Verb-Object model
        generated from Stanford Parser

        :param comments: List of tuples containing 'comment', 'vote', and 'timestamp'
        fields; 'comment' is a string and 'vote' and 'timestamps' are integers
        
        :return phrases: List of dictionaries containing 'phrase', 'vote', and 'timestamp'
        fields; 'phrase' is a string and 'vote' and 'timestamp' are integers
        """
        # Grab comments that have specific word
        # Parse through comments using Subject-Predicate-Object and split comment into phrases
        phrases = []    # list of dicts: 'phrase', 'vote'

        for comment in comments:
            #list of lists 0 is comment 1 is vote
            sentence = comment[0].split(".")
            vote = comment[1]
            timestamp = comment[2]
            for sent in sentence:
                phrase = re.split('; |, | and | but | or | nor ', sent)

                # val = []
                # for sent in sentences:
                #     root_tree = svo.get_parse_tree(sent)
                #     val.append(svo.process_parse_tree(next(root_tree)))

                # subject = ""
                # predicate = ""
                # obj = ""
                # org_phrase = ""

                # list_phrase = []
                # for ind, j in enumerate(val):
                #     new_phrase = ""
                #     if j:
                #         i = j[0]
                #         subject = i["subject"][0]
                #         predicate = i["predicate"][0]
                #         obj = i["object"][0]
                #         list_phrase.append(sentences[ind])
                #         org_phrase = sentences[ind]
                #     else:
                #         new_phrase = org_phrase.replace(obj, sentences[ind])
                #         list_phrase.append(new_phrase)
                # print(list_phrase)
                # print()

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
        
        :return phrases: List of dictionaries containing 'phrase','vote' and 'timestamps'
        fields; 'phrase' is a string and 'vote' and 'timestamps' are integers
        """
        # Run it through the SentimentIntensityAnalyzer
        related_phrases = []
        for d in self.comments_:
            if word.lower() in d['phrase'].lower():
                related_phrases.append(d)

        sentiment_values = []
        for i in related_phrases:
            vs = self.model_.polarity_scores(i['phrase'])
            sentiment_values.append({'score': vs['compound'], 'vote': i['vote'],
                'timestamp': i['timestamp'], 'word': word})
            
        return sentiment_values

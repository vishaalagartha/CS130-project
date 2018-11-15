# https://github.com/cjhutto/vaderSentiment#python-code-example
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

class SentimentModel:
    def __init__(self, comments, params):
        self.comments_ = self.handleComments(comments)
        self.model_ = SentimentIntensityAnalyzer()
        self.params_ = params

    def handleComments(self, comments):
        # Get comments
        # Grab comments that have specific word
        print('handling comments')
        
        #parse through comments using Subject-Predicate-Object and split comment into phrases
        #still under work

        #return phrases.
        phrases = []
        for i in comments:
            phrase = re.split('; |, |and |but |or |nor ',i)

            for j in phrase:
                phrases.append(j)
        return phrases  

    def generateSentiments(self, sentences):
        print('generating sentiments')
        # Run it through the SentimentIntensityAnalyzer
        related_phrases = []
        for phrase in self.comments_:
            if word.lower() in phrase.lower():
                related_phrases.append(phrase)
        print(related_phrases)

        for i in related_phrases:
            vs = self.model_.polarity_scores(i)
            print("{:-<65} {}".format(i, str(vs)))

    def sendSentiments(self):
        print('sending sentiments')

# https://github.com/cjhutto/vaderSentiment#python-code-example
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SentimentModel:
    def __init__(self, comments, params):
        self.comments_ = self.handleComments(comments)
        self.model_ = SentimentIntensityAnalyzer()
        self.params_ = params

    def handleComments(self, comments):
        # Get comments
        # Grab comments that have specific word

        #parse through comments using Subject-Predicate-Object and split comment into phrases
        #still under work

        #return phrases.
        phrases = []
        for comment in comments:
            phrase = re.split('; |, |and |but |or |nor ', comment)
            # phrases.append([word for word in phrase])

            for j in phrase:
                phrases.append(j)
        return phrases  

    def generateSentiments(self, word):
        # Run it through the SentimentIntensityAnalyzer
        related_phrases = []
        for phrase in self.comments_:
            if word.lower() in phrase.lower():
                related_phrases.append(phrase)

        # sentiment_values = []
        for i in related_phrases:
            vs = self.model_.polarity_scores(i)
            # sentiment_values.append(vs)
            print("{:-<65} {}".format(i, str(vs)))

        # return sentiment_values

    def sendSentiments(self):
        print('sending sentiments')
        #to be implement after talking with front end team members
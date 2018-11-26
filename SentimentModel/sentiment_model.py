# https://github.com/cjhutto/vaderSentiment#python-code-example
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

class SentimentModel:
    def __init__(self, comments, params):
        self.comments_ = self.handleComments(comments)
        self.model_ = SentimentIntensityAnalyzer()
        self.params_ = params

    def handleComments(self, comments):
        # Grab comments that have specific word
        #parse through comments using Subject-Predicate-Object and split comment into phrases
        #still under work

        #return phrases.
        phrases = []    # list of dicts: 'phrase', 'vote'


        for comment in comments:
            #list of lists 0 is comment 1 is vote
            sentence = comment[0].split(".")
            vote = comment[1]
            for i in sentence:
                phrase = re.split('; |, | and | but | or | nor ', i)
            # phrases.append([word for word in phrase])

                for j in phrase:
                    phrases.append({'phrase': j, 'vote': vote})
        return phrases  

    def generateSentiments(self, word):
        # Run it through the SentimentIntensityAnalyzer
        related_phrases = []
        for d in self.comments_:
            if word.lower() in d['phrase'].lower():
                related_phrases.append(d)

        # sentiment_values = []
        avg = 0
        for i in related_phrases:
            vs = self.model_.polarity_scores(i['phrase'])
            # sentiment_values.append(vs)
            # print("{:-<65} {}".format(i['phrase'], str(vs['compound']*i['vote'])))
            avg += vs['compound']*i['vote']

        if related_phrases:
            score = avg / len(related_phrases)
            if score >= 0.05:
                print('Positive')
            elif score <= -0.05:
                print('MEGATIVE')
            else:
                print('Neutral')

        # return sentiment_values

    def sendSentiments(self):
        print('sending sentiments')
        #to be implement after talking with front end team members

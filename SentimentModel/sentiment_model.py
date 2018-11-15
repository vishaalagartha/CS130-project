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
        #return phrases.

        comments_ = ["VADER is smart, VADER is handsome, and VADER is funny.",  # positive sentence example
             "VADER is smart, VADER is handsome, and VADER is funny!",  # punctuation emphasis handled correctly (sentiment intensity adjusted)
             "VADER is very smart, and Vader is very handsome and Vader is very funny.", # booster words handled correctly (sentiment intensity adjusted)
             "VADER is VERY SMART, VADER is VERY handsome, and VADER is VERY FUNNY.",  # emphasis for ALLCAPS handled
             "VADER is VERY SMART, VADER is VERY handsome, and VADER is VERY FUNNY!!!", # combination of signals - VADER appropriately adjusts intensity
             "VADER is VERY SMART, VADER is uber handsome, and VADER is FRIGGIN FUNNY!!!", # booster words & punctuation make this close to ceiling for score
             "VADER is not smart, VADER is not handsome, VADER is not funny.",  # negation sentence example
             "The book was good.",  # positive sentence
             "At least it isn't a horrible book.",  # negated negative sentence with contraction
             "The book was only kind of good.", # qualified positive sentence is handled correctly (intensity adjusted)
             "The plot was good, but the characters are uncompelling and the dialog is not great.", # mixed negation sentence
             "Today SUX!",  # negative slang with capitalization emphasis
             "Today only kinda sux! But I'll get by, lol", # mixed sentiment example with slang and constrastive conjunction "but"
             "Make sure you :) or :D today!",  # emoticons handled
             "Catch utf-8 emoji such as such as 💘 and 💋 and 😁",  # emojis handled
             "Not bad at all",  # Capitalized negation,
             ]
        print(comments_)
        return comments_  

    def generateSentiments(self, sentences):
        print('generating sentiments')
        # Run it through the SentimentIntensityAnalyzer
        for sentence in sentences:
            vs = self.model_.polarity_scores(sentence)
            print("{:-<65} {}".format(sentence, str(vs)))
            print()

    def sendSentiments(self):
        print('sending sentiments')

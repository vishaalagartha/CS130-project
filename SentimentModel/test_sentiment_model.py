import unittest
from sentiment_model import SentimentModel

class TestSentimentModel(unittest.TestCase):
    def setUp(self):
        self.vader_comments = ["VADER is smart, handsome, and funny.",  # positive sentence example
             "VADER is smart, handsome, and funny!",  # punctuation emphasis handled correctly (sentiment intensity adjusted)
             "VADER is very smart, handsome, and funny.", # booster words handled correctly (sentiment intensity adjusted)
             "VADER is VERY SMART, handsome, and FUNNY.",  # emphasis for ALLCAPS handled
             "VADER is VERY SMART, handsome, and FUNNY!!!", # combination of signals - VADER appropriately adjusts intensity
             "VADER is VERY SMART, uber handsome, and FRIGGIN FUNNY!!!", # booster words & punctuation make this close to ceiling for score
             "VADER is not smart, handsome, nor funny.",  # negation sentence example
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
        self.comment_1 = ['I love eating lakers and cookies!']
        self.comment_2 = ['I am extremely exhausted and I want to sleep']
        self.comment_3 = ['cookies are life but cs181 is not']
        self.params = {}
        self.model = SentimentModel(self.vader_comments, self.params)

    def test_handle_comments(self):
        self.assertEqual(self.model.handleComments(self.comment_1), ['I love eating lakers ', 'cookies!'])
        self.assertEqual(self.model.handleComments(self.comment_2), ['I am extremely exhausted ', 'I want to sleep'])
        self.assertEqual(self.model.handleComments(self.comment_3), ['cookies are life ', 'cs181 is not'])

    def test_generate_sentiments(self):
        print('Testing generateSentiments with word: vader')
        self.model.generateSentiments('vader')
        print()

        print('Testing generateSentiments with word: book')
        self.model.generateSentiments('book')

if __name__ == '__main__':
    unittest.main()
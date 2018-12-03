import unittest
from sentiment_model import SentimentModel

class TestSentimentModel(unittest.TestCase):
    def setUp(self):
        self.vader_comments = [
             ('VADER is smart, handsome, and funny.', 2, 1541500070),  # positive sentence example
             ('VADER is smart, handsome, and funny!', 3, 1541500071),  # punctuation emphasis handled correctly (sentiment intensity adjusted)
             ('VADER is very smart, handsome, and funny.', 4, 1541500072), # booster words handled correctly (sentiment intensity adjusted)
             ('VADER is VERY SMART, handsome, and FUNNY.', 2, 1541500073),  # emphasis for ALLCAPS handled
             ('VADER is VERY SMART, handsome, and FUNNY!!!', 3, 1541500074), # combination of signals - VADER appropriately adjusts intensity
             ('VADER is VERY SMART, uber handsome, and FRIGGIN FUNNY!!!', 4, 1541500075), # booster words & punctuation make this close to ceiling for score
             ('VADER is not smart, handsome, nor funny.', 2, 541500076),  # negation sentence example
             ('The book was good.', 3, 1541500077),  # positive sentence
             ("At least it isn't a horrible book.", 4, 1541500078),  # negated negative sentence with contraction
             ("The book was only kind of good.", 2, 1541500079), # qualified positive sentence is handled correctly (intensity adjusted)
             ("The plot was good, but the characters are uncompelling and the dialog is not great.", 3, 1541500080), # mixed negation sentence
             ("Today SUX!", 3, 1541500081),  # negative slang with capitalization emphasis
             ("Today only kinda sux! But I'll get by, lol", 4, 1541500082), # mixed sentiment example with slang and constrastive conjunction "but"
             ("Make sure you :) or :D today!", 2, 1541500083),  # emoticons handled
             ("Catch utf-8 emoji such as such as 💘 and 💋 and 😁", 3, 1541500084),  # emojis handled
             ("Not bad at all", 4, 1541500085),  # Capitalized negation,
             ]
        self.comment_1 = [('I love eating lakers and cookies!', 78, 1530000051)]
        self.comment_2 = [('I am extremely exhausted and I want to sleep', 32, 1541600088)]
        self.comment_3 = [('cookies are life but cs181 is not', 100, 1541500088)]
        self.model = SentimentModel(self.vader_comments)

    def test_handle_comments(self):
        self.assertEqual(self.model.handleComments(self.comment_1), 
                                                   [{'phrase': 'I love eating lakers', 'vote': self.comment_1[0][1], 'timestamp': self.comment_1[0][2]},
                                                    {'phrase': 'cookies!', 'vote': self.comment_1[0][1], 'timestamp': self.comment_1[0][2]}])
        self.assertEqual(self.model.handleComments(self.comment_2), 
                                                   [{'phrase': 'I am extremely exhausted', 'vote': self.comment_2[0][1], 'timestamp': self.comment_2[0][2]},
                                                    {'phrase': 'I want to sleep', 'vote': self.comment_2[0][1], 'timestamp': self.comment_2[0][2]}])
        self.assertEqual(self.model.handleComments(self.comment_3), 
                                                   [{'phrase': 'cookies are life', 'vote': self.comment_3[0][1], 'timestamp': self.comment_3[0][2]},
                                                    {'phrase': 'cs181 is not', 'vote': self.comment_3[0][1], 'timestamp': self.comment_3[0][2]}])

    def test_generate_sentiments(self):
        print('Testing generateSentiments with word: vader')
        print(self.model.generateSentiments('vader'))
        print()

        print('Testing generateSentiments with word: book')
        print(self.model.generateSentiments('book'))

if __name__ == '__main__':
    unittest.main()

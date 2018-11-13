import nltk.classify.util
import words
#from data_crawler import DataCrawler
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import names


def word_feats(words):
    return dict([(word, True) for word in words])


#params = {'subreddit': 'politics', 'start': 1541700088, 'end': 1541700188}
#crawler = DataCrawler(params)
#freqs = crawler.run()
#print(freqs)
 
# positive_vocab = [ 'awesome', 'outstanding', 'fantastic', 'terrific', 'good', 'nice', 'great', '🙂' ]
# negative_vocab = [ 'bad', 'terrible','useless', 'hate', '😞' ]
positive_vocab = words.POSITIVE_WORDS
negative_vocab = words.NEGATIVE_WORDS

positive_features = [(word_feats(pos), 'pos') for pos in positive_vocab]
negative_features = [(word_feats(neg), 'neg') for neg in negative_vocab]

 
# Predict
neg = 0
pos = 0
# sentence = "Bad movie, a hate it. terrible"
sentence = 'All work and no play makes jack dull boy. All work and no play makes jack a dull boy.'
sentence = sentence.lower()
words = sentence.split(' ')
neutral_vocab=[]
for word in words:
	if word not in positive_vocab:
		if word not in negative_vocab:
			neutral_vocab.append(word)

neutral_features = [(word_feats(neu), 'neu') for neu in neutral_vocab]
 
train_set = negative_features + positive_features + neutral_features
classifier = NaiveBayesClassifier.train(train_set) 

for word in words:
	if len(word) > 1:
		classResult = classifier.classify( word_feats(word))
		if classResult == 'neg':
			neg = neg + 1
		if classResult == 'pos':
			pos = pos + 1
 
print('Positive: ' + str(float(pos)/len(words)))
print('Negative: ' + str(float(neg)/len(words)))
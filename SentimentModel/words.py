import numpy as np
import pandas as pd

positive = pd.read_csv('positive-words.csv', header=None, dtype=str)
negative = pd.read_csv('negative-words.csv', header=None, dtype=str)

POSITIVE_WORDS = [words[0] for words in positive.values]
NEGATIVE_WORDS = [words[0] for words in negative.values]

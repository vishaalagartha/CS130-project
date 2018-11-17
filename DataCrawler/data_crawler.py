import string, json, requests
from constants import COMMON_WORDS 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from operator import itemgetter

class DataCrawler:
    def __init__(self, params):
        self.subreddit = params['subreddit'] 
        self.start_date = params['start']
        self.end_date = params['end']

    def fetch(self):
        last_date = self.start_date
        text = ''
        comments = []

        while last_date<=self.end_date:
            query_str = 'https://api.pushshift.io/reddit/search/comment/?subreddit=' \
            + str(self.subreddit) \
            + '&after=' + str(last_date) \
            + '&before=' + str(self.end_date) \
            + '&size=500'

            resp = requests.get(query_str)

            data = resp.json()['data']
            for comment in data:
                if comment['created_utc']>last_date:
                    last_date = comment['created_utc']
                text+=(comment['body'] + ' ')
                c = comment['body'].replace('\n', '').replace('\r', '')
                comments.append((c, comment['score']))

            if len(data)==0:
                break

        return text, comments

    def filter_words(self, text):
        # split into words
        tokens = word_tokenize(text)
        # convert to lower case
        tokens = [w.lower() for w in tokens]
        # remove punctuation from each word
        table = str.maketrans('', '', string.punctuation)
        stripped = [w.translate(table) for w in tokens]
        # remove remaining tokens that are not alphabetic
        words = [word for word in stripped if word.isalpha()]
        # filter out stop words
        stop_words = set(stopwords.words('english'))
        words = [w for w in words if not w in stop_words]

        return words

    def count_freq(self, words):
        d = {}
        word_count = 0
        for w in words:
            if w not in d:
                d[w] = 0
                word_count += 1
            d[w] += 1

        sorted_d = sorted(d.items(), key=itemgetter(1))[::-1]

        return sorted_d

    def run(self):
        all_text, comments = self.fetch()
        filtered_words = self.filter_words(all_text)
        freq = self.count_freq(filtered_words)

        return freq, comments

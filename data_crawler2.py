import string, json
from multiprocessing import Pool
from psaw import PushshiftAPI
from constants import COMMON_WORDS 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from operator import itemgetter

class DataCrawler:
    def __init__(self, params):
        self.subreddit = params['subreddit'] 
        self.start_date = params['start']
        self.end_date = params['end']
        self.api = PushshiftAPI()

        # calculate number of threads
        nthreads = 5
        size = int((self.end_date-self.start_date)/nthreads)
        self.date_ranges = []
        end_date = self.end_date
        while end_date>self.start_date:
            self.date_ranges.append({'after': end_date-size, 'before': end_date})
            end_date -= size

    def fetch(self, ranges):
        gen =  self.api.search_comments(subreddit=self.subreddit, before=ranges['before'],
                after=ranges['after'])

        batch_count = 0
        text = ''
        # generator returns in batches of 50
        for g in gen:
            try:
                text+=(g.body+' ')
            except:
                pass
        return text

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
        with Pool(len(self.date_ranges)) as p:
            l = p.map(self.fetch, self.date_ranges)
        all_text = ''.join(l)
        
        filtered_words = self.filter_words(all_text)

        freq = self.count_freq(filtered_words)

        return freq


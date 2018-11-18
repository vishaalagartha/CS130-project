import asyncio, string, json, requests
from functools import partial
from constants import COMMON_WORDS 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from operator import itemgetter

class DataCrawler:
    def __init__(self, params):
        self.subreddit = params['subreddit'] 
        self.start_date = params['start']
        self.end_date = params['end']

    def fetch(self, date_range):
        last_date = date_range['after']
        text = ''
        comments = []

        while last_date<=date_range['before']:
            query_str = 'https://api.pushshift.io/reddit/search/comment/?subreddit=' \
            + str(self.subreddit) \
            + '&after=' + str(last_date) \
            + '&before=' + str(date_range['before']) \
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

    def get_num_comments(self):
        query_str = 'https://api.pushshift.io/reddit/search/comment/?subreddit=' \
        + str(self.subreddit) \
        + '&after=' + str(self.start_date) \
        + '&before=' + str(self.end_date) \
        + '&aggs=created_utc&size=0' 

        resp = requests.get(query_str)
        data = resp.json()['aggs']['created_utc']

        num_comments = 0
        for d in data:
            num_comments+=d['doc_count']

        return num_comments

    def get_date_ranges(self, num_comments):
        # set each thread to make 1 get
        num_requests = 2
        # set chunk_size
        nthreads = num_comments/(500*num_requests)
        
        chunk_size = int((self.end_date-self.start_date)/nthreads)
        date_ranges = []
        end_date = self.end_date
        while end_date>self.start_date:
            date_ranges.append({'after': end_date-chunk_size, 'before': end_date})
            end_date -= chunk_size 

        return date_ranges

    async def run(self):

        num_comments = self.get_num_comments()
        ranges = self.get_date_ranges(num_comments)
        print(ranges)
        futures = [loop.run_in_executor(None, partial(self.fetch, r)) \
                for r in ranges]
        results = await asyncio.gather(*futures)
        for (i, result) in zip(ranges, results):
                print(i, result)


        '''
        all_text, comments = self.fetch()
        filtered_words = self.filter_words(all_text)
        freq = self.count_freq(filtered_words)

        return freq, comments
        '''

params = {'subreddit': 'nba', 'start': 1542559020, 'end': 1542559028}
d = DataCrawler(params)

loop = asyncio.get_event_loop()
loop.run_until_complete(d.run())

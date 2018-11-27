"""
The DataCrawler class can be used to asynchronously fetch comments from a
specific subreddit between two timestamps.
"""

import asyncio, string, json, requests, time, math
from functools import partial
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from operator import itemgetter

class DataCrawler:
    """
    Encapsulates an instance of the DataCrawler class
    """
    def __init__(self, params):
        """
        Construct a new instance of a DataCrawler

        :param params: Dictionary containing a 'subreddit', 'start', and 'end'
        field; 'subreddit' is a string; 'start' and 'end' are integer
        timestamps.
        :return: returns None
        """
        self.subreddit = params['subreddit'] 
        self.start_date = params['start']
        self.end_date = params['end']

    def fetch(self, date_range):
        """
        Fetches comments between a range of dates.

        :param date_range: Dictionary containing 'after' and 'before' field both
        of type integer
        :return text, comments: Where text is a string containing all comments
        and comments is a list of tuples containing 2 elements. The first
        element is a string containing the comment and the second element is the
        number of upvotes for the comment.
        """
        last_date = date_range['after']
        text = ''
        comments = []

        # Each query returns 500 comments, so keep querying until we receive no
        # data
        while last_date<=date_range['before']:
            query_str = 'https://api.pushshift.io/reddit/search/comment/?subreddit=' \
            + str(self.subreddit) \
            + '&after=' + str(last_date) \
            + '&before=' + str(date_range['before']) \
            + '&size=500'

            resp = requests.get(query_str)

            if resp.status_code==200:
                data = resp.json()['data']
                for comment in data:
                    if comment['created_utc']>last_date:
                        # update last date for next GET
                        last_date = comment['created_utc']
                    text+=(comment['body'] + ' ')
                    c = comment['body'].replace('\n', '').replace('\r', '')
                    comments.append((c, comment['score']))

                if len(data)==0:
                    break

        return text, comments

    def filter_words(self, text):
        """
        Converts text into individual words, formats the words, and removes all
        stop words

        :param text: A long string containing all the text
        :return words: A list of formatted and filtered words
        """
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
        """
        Counts the number of occurrences of each word

        :param words: A list of words
        :return sorted_d: A list of tuples containing the word and number of
        occurrences, sorted by frequency
        """
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
        """
        Use aggs from PushshiftAPI() to make 1 query to obtain the number of
        comments in date range

        :param: No parameters
        :return num_comments: Total number of comments in date range
        """
        query_str = 'https://api.pushshift.io/reddit/search/comment/?subreddit=' \
        + str(self.subreddit) \
        + '&after=' + str(self.start_date) \
        + '&before=' + str(self.end_date) \
        + '&aggs=created_utc&size=0' 

        resp = requests.get(query_str)
        num_comments = 0
        if resp.status_code==200:
            data = resp.json()['aggs']['created_utc']
            for d in data:
                num_comments+=d['doc_count']

        return num_comments

    def get_date_ranges(self, num_comments):
        """
        Based on number of comments, set the date ranges each thread will GET
        for.

        :param num_comments: Total number of comments to fetch
        :return date_ranges: A list of objects containing an 'after' and 'before'
        field. Each thread obtains comments between these two dates.
        """
        # set each thread to make 1 get
        num_requests = 1
        # set chunk_size
        nthreads = 1 if num_comments==0 else int(math.ceil(num_comments/(500*num_requests)))
        
        chunk_size = int((self.end_date-self.start_date)/nthreads)
        date_ranges = []
        after = self.start_date
        before = self.start_date+chunk_size
        while before<=self.end_date:
            date_ranges.append({'after': after, 'before': before})
            after+=chunk_size
            before+=chunk_size

        if before<self.end_date:
            date_ranges.append({'after': before, 'before': self.end_date})

        return date_ranges

    async def async_fetch(self):
        """
        Asynchronously fetch and gather all text and comments for a specific
        thread
        
        :param: No parameters
        :return freq, comments: A list of tuples containing filtered words and
        frequencies and a list of tuples containing individual comments
        and upvotes.
        """
        num_comments = self.get_num_comments()
        ranges = self.get_date_ranges(num_comments)
        futures = [self.loop.run_in_executor(None, partial(self.fetch, r)) \
                for r in ranges]
        results = await asyncio.gather(*futures)
        all_text = ''
        comments = []
        for r in results:
            all_text+=(r[0] + ' ')
            comments+=r[1]
        filtered_words = self.filter_words(all_text)
        freq = self.count_freq(filtered_words)

        return freq, comments

    def run(self):
        """
        Main function to asynchronously fetch frequencies and comments

        :param: No parameters
        :return freq, comments: A list of tuples containing filtered words and
        frequencies and a list of tuples containing individual comments
        and upvotes.
        """
        self.loop = asyncio.get_event_loop()
        freq, comments = self.loop.run_until_complete(self.async_fetch())

        return freq, comments

"""
Unit tests for DataCrawler module
"""
import unittest, requests, json, threading, asyncio
from data_crawler import DataCrawler
from http.server import HTTPServer, BaseHTTPRequestHandler
from server import RequestHandler

def start_server(server):
    asyncio.set_event_loop(asyncio.new_event_loop())
    server.serve_forever()


class TestDataCrawler(unittest.TestCase):
    """
    Test cases for the DataCrawler class. This class subclasses from
    unittest.TestCase
    """
    def test_server(self):
        server_port = 8080

        server = HTTPServer(('', server_port), RequestHandler)
        server_thread = threading.Thread(target=start_server, args=(server,))
        server_thread.daemon = True
        server_thread.start()

        r = requests.post('http://127.0.0.1:8080', json={'subreddit': 'nba',
            'start': 1541266100, 'end': 1541266115})

        for w in r.json():
            self.assertTrue('word' in w and isinstance(w['word'], str))
            self.assertTrue('timestamps' in w and isinstance(w['timestamps'], list))
            self.assertTrue('score' in w and isinstance(w['score'], list))
            self.assertTrue('frequency' in w and isinstance(w['frequency'], int))

        self.assertEqual(200, r.status_code)

        r = requests.post('http://127.0.0.1:8080', json={'subreddit': 'nba',
            'start': 1541246800})

        self.assertEqual(400, r.status_code)

        r = requests.post('http://127.0.0.1:8080', json={'subreddit': 'nba',
            'start': 'hello this is bad', 'end': 1541266115})

        self.assertEqual(400, r.status_code)

        r = requests.post('http://127.0.0.1:8080', json={'subreddit': [1, 2, 3],
            'start': 'hello this is bad', 'end': 1541266115})

        self.assertEqual(400, r.status_code)
        server.shutdown()

    def test_filter_words(self):
        """
        Test if words are filtered properly by the DataCrawler. Words should be
        tokenized, unpunctuated, uncapitalized, and filtered to remove stopwords

        :return: Returns none
        """
        params = {'subreddit': 'nba', 'start': 10000, 'end': 20000}
        crawler = DataCrawler(params)
        unfiltered = 'All work and no play makes jack dull boy. All work and no play makes jack a dull boy.'
        filtered = ['work', 'play', 'makes', 'jack', 'dull', 'boy', 'work', 'play', 'makes', 'jack', 'dull', 'boy']
        result = crawler.filter_words(unfiltered) 

        self.assertListEqual(result, filtered)


    def test_count_freqs(self):
        """
        Test if words are counted properly.

        :return: Returns none
        """
        params = {'subreddit': 'nba', 'start': 10000, 'end': 20000}
        crawler = DataCrawler(params)

        words = ['hello']*5 + ['world']*20 + ['my'] + ['name']*3 + ['vishaal']*100
        freqs = [('vishaal', 100), ('world', 20), ('hello', 5), ('name', 3), ('my', 1)]
        result = crawler.count_freqs(words)

        self.assertListEqual(result, freqs)

    def test_subreddits(self):
        """
        Test if individual subreddits have high frequencies of relevant words.

        :return: Returns none
        """

        # Test 1: r/politics should have 'trump' more than 20 times, with a high
        # average score
        params = {'subreddit': 'politics', 'start': 1541700088, 'end': 1541700188}
        crawler = DataCrawler(params)
        sentiments = crawler.run()
        has_trump = False
        for i in sentiments:
            if i['word']=='trump' and i['frequency']>20:
                has_trump = True
        self.assertTrue(has_trump)

        # Test 2: r/javascript should have 'code' more than 50 times, with a
        # high average score
        params = {'subreddit': 'javascript', 'start': 1541600088, 'end': 1541700188}
        crawler = DataCrawler(params)
        sentiments = crawler.run()
        has_code = False
        for i in sentiments:
            if i['word']=='code' and i['frequency']>50:
                has_code = True
        self.assertTrue(has_code)

        # Test 3: r/ucla should have 'quarter' more than 50 times, with a high
        # average score
        params = {'subreddit': 'ucla', 'start': 1541500088, 'end': 1541700188}
        crawler = DataCrawler(params)
        sentiments = crawler.run()
        for i in sentiments:
            if i['word']=='quarter' and i['frequency']>20:
                has_quarter = True
        self.assertTrue(has_quarter)

    def test_backend(self):
        """
        Test if individual subreddits have appropriate average scores for
        relevant words.

        :return: Returns none
        """
        # Test 1: r/warriors sentiments toward 'curry', 'klay', 'lebron',
        # 'draymond'
        params = {'subreddit': 'warriors', 'start': 1541600088, 'end': 1541700188}
        crawler = DataCrawler(params)
        sentiments = crawler.run()
        for i in sentiments:
            if i['word']=='curry':
                avg_score_curry = sum(i['score'])/i['frequency']
            if i['word']=='klay':
                avg_score_klay = sum(i['score'])/i['frequency']
            if i['word']=='lebron':
                avg_score_lebron = sum(i['score'])/i['frequency']
            if i['word']=='draymond':
                avg_score_draymond = sum(i['score'])/i['frequency']

        self.assertGreater(avg_score_curry, 0)
        self.assertGreater(avg_score_klay, 0)
        self.assertGreater(avg_score_lebron, 0)
        self.assertLess(avg_score_draymond, 0)

        # Test 2: r/tesla sentiments toward 'musk'
        params = {'subreddit': 'tesla', 'start': 1530000051, 'end': 1541800288}
        crawler = DataCrawler(params)
        sentiments = crawler.run()
        for i in sentiments:
            if i['word']=='musk':
                avg_score_musk = sum(i['score'])/i['frequency']
        self.assertLess(avg_score_musk, 0.1)

        # Test 3: r/stocks sentiments toward 'cannabis', 'apple', and 'amazon'
        params = {'subreddit': 'stocks', 'start': 1541500088, 'end': 1541700188}
        crawler = DataCrawler(params)
        sentiments = crawler.run()
        for i in sentiments:
            if i['word']=='cannabis':
                avg_score_cannabis = sum(i['score'])/i['frequency']
            if i['word']=='apple':
                avg_score_apple = sum(i['score'])/i['frequency']
            if i['word']=='amazon':
                avg_score_amazon = sum(i['score'])/i['frequency']
        self.assertGreater(avg_score_cannabis, 0.0)
        self.assertGreater(avg_score_apple, 0.0)
        self.assertGreater(avg_score_amazon, 0.1)


if __name__ == '__main__':
    unittest.main()

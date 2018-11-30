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

        # Test 1: r/politics should have 'trump' more than 20 times
        params = {'subreddit': 'politics', 'start': 1541700088, 'end': 1541700188}
        crawler = DataCrawler(params)
        sentiments = crawler.run()
        has_trump = False
        for i in sentiments:
            if i['word']=='trump' and i['frequency']>20:
                avg_score = sum(i['score'])/i['frequency']
                has_trump = True
        self.assertLess(avg_score, 0)
        self.assertTrue(has_trump)

        # Test 2: r/javascript should have 'code' more than 50 times
        params = {'subreddit': 'javascript', 'start': 1541600088, 'end': 1541700188}
        crawler = DataCrawler(params)
        sentiments = crawler.run()
        has_code = False
        for i in sentiments:
            if i['word']=='code' and i['frequency']>50:
                avg_score = sum(i['score'])/i['frequency']
                has_code = True
        self.assertGreater(avg_score, 0.1)
        self.assertTrue(has_code)

        # Test 3: r/ucla should have 'quarter' more than 50 times
        params = {'subreddit': 'ucla', 'start': 1541500088, 'end': 1541700188}
        crawler = DataCrawler(params)
        sentiments = crawler.run()
        for i in sentiments:
            if i['word']=='quarter' and i['frequency']>20:
                avg_score = sum(i['score'])/i['frequency']
                has_quarter = True
        self.assertGreater(avg_score, 0)
        self.assertTrue(has_quarter)


if __name__ == '__main__':
    unittest.main()

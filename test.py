import unittest, requests
from data_crawler2 import DataCrawler

class TestDataCrawler(unittest.TestCase):
    def test_server(self):
        r = requests.post('http://127.0.0.1:8080', json={'subreddit': 'nba',
            'start': 1541266110, 'end': 1541266115})

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


    def test_filter_words(self):
        params = {'subreddit': 'nba', 'start': 10000, 'end': 20000}
        crawler = DataCrawler(params)
        unfiltered = 'All work and no play makes jack dull boy. All work and no play makes jack a dull boy.'
        filtered = ['work', 'play', 'makes', 'jack', 'dull', 'boy', 'work', 'play', 'makes', 'jack', 'dull', 'boy']
        result = crawler.filter_words(unfiltered) 

        self.assertListEqual(result, filtered)

    def test_count_freq(self):
        params = {'subreddit': 'nba', 'start': 10000, 'end': 20000}
        crawler = DataCrawler(params)

        words = ['hello']*5 + ['world']*20 + ['my'] + ['name']*3 + ['vishaal']*100
        freqs = [('vishaal', 100), ('world', 20), ('hello', 5), ('name', 3), ('my', 1)]
        result = crawler.count_freq(words)

        self.assertListEqual(result, freqs)

    def test_subreddits(self):
        params = {'subreddit': 'politics', 'start': 1541700088, 'end': 1541700188}
        crawler = DataCrawler(params)
        freqs = crawler.run()
        for word in freqs:
            if word[0]=='trump':
                word_that_should_exist = word

        self.assertEqual(word_that_should_exist[0], 'trump')
        self.assertGreaterEqual(word_that_should_exist[1], 20) 

        params = {'subreddit': 'javascript', 'start': 1541600088, 'end': 1541700188}
        crawler = DataCrawler(params)
        freqs = crawler.run()
        for word in freqs:
            if word[0]=='code':
                word_that_should_exist = word

        self.assertEqual(word_that_should_exist[0], 'code')
        self.assertGreaterEqual(word_that_should_exist[1], 50) 

        params = {'subreddit': 'ucla', 'start': 1541500088, 'end': 1541700188}
        crawler = DataCrawler(params)
        freqs = crawler.run()
        for word in freqs:
            if word[0]=='quarter':
                word_that_should_exist = word

        self.assertEqual(word_that_should_exist[0], 'quarter')
        self.assertGreaterEqual(word_that_should_exist[1], 20) 




if __name__ == '__main__':
    unittest.main()

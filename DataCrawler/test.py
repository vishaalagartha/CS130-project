import unittest, requests, json, threading
from functools import partial
from data_crawler import DataCrawler
from http.server import HTTPServer, BaseHTTPRequestHandler
from server import RequestHandler

class TestServer(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length).decode('utf-8'))
        expected_data = [["I guess we'll see", 1], 
        ['chandler is like 93% tatoos', 1], 
        ['Lol you think it’ll take two months', 1], 
        ["""This is the problem with the max contracts. It means that a guy like
        John Wall or Kyle Lowry are worth the same as Lebron or KD. 
                Which is kind of nuts. I feel like it'd help league parity if 
                they uncapped contracts, and just told players you can get paid 
                99.9% of your teams cap, but enjoy being on the shittiest team 
                in basketball. Then you'd get guys to spread out and go for 
                their money while others decide they'll take a more moderate 
                amount to have a good team.  """, 1], ["""All teams have unluckiness 
                of injuries or losing to better teams. Saying that Cleveland 
                wasnt lucky because of those two things doesn't negate the luck 
                of getting a LeBron or having 3 number one picks in 4 years. """,
                1], ["""90s Bulls were nowhere near this level of everyone 
                    thinking they're shoe-ins for the finals and a title.""", 1],
                ["""This is just how the NBA is. If you don't like it then you 
                    need to find other entertainment options.  You can't have 
                    parity in a winter sport where certain markets have snow and 
                    certain markets don't.""", 1]]

        if len(expected_data)==len(post_data):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
        else:
            self.send_response(400, 'Bad data provided')


class TestDataCrawler(unittest.TestCase):
    def test_server(self):
        server_port = 8080
        test_server_port = 8081

        handler = partial(RequestHandler, True)
        server = HTTPServer(('', server_port), handler)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True

        test_server = HTTPServer(('', test_server_port), TestServer)
        test_server_thread = threading.Thread(target=test_server.serve_forever)
        test_server_thread.daemon = True


        server_thread.start()
        test_server_thread.start()

        r = requests.post('http://127.0.0.1:8080', json={'subreddit': 'nba',
            'start': 1541266100, 'end': 1541266115})
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
        test_server.shutdown()


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
        freqs, comments = crawler.run()
        for word in freqs:
            if word[0]=='trump':
                word_that_should_exist = word

        self.assertEqual(word_that_should_exist[0], 'trump')
        self.assertGreaterEqual(word_that_should_exist[1], 20) 

        params = {'subreddit': 'javascript', 'start': 1541600088, 'end': 1541700188}
        crawler = DataCrawler(params)
        freqs, comments = crawler.run()
        for word in freqs:
            if word[0]=='code':
                word_that_should_exist = word

        self.assertEqual(word_that_should_exist[0], 'code')
        self.assertGreaterEqual(word_that_should_exist[1], 50) 

        params = {'subreddit': 'ucla', 'start': 1541500088, 'end': 1541700188}
        crawler = DataCrawler(params)
        freqs, comments = crawler.run()
        for word in freqs:
            if word[0]=='quarter':
                word_that_should_exist = word

        self.assertEqual(word_that_should_exist[0], 'quarter')
        self.assertGreaterEqual(word_that_should_exist[1], 20) 

if __name__ == '__main__':
    unittest.main()

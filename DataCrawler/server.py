"""
The RequestHandler module serves POST requests to fetch frequencies and
comments from the DataCrawler class and forwards the results to the WordCloud
and SentimentAnalyzer modules.
"""
import sys, json, http.client
from data_crawler import DataCrawler
from http.server import HTTPServer, BaseHTTPRequestHandler


class RequestHandler(BaseHTTPRequestHandler):
    """
    Encapsulates an instance of the RequestHandler class. This class subclasses
    http.server's BaseHTTPRequestHandler.
    """
    def __init__(self, *args, **kwargs):
        """
        Construct a new instance of RequestHandler

        :return: Returns none
        """
        super().__init__(*args, **kwargs)

    def validated(self, post_data):
        """
        Validate post data by checking if 'subreddit', 'start', and 'end' fields
        exist and have appropriate types

        :param post_data: Object containing parameters for creating a
        DataCrawler instance
        :return valid: Whether or not post data is valid
        """
        if 'subreddit' not in post_data or not isinstance(post_data['subreddit'], str):
            return False
        if 'start' not in post_data or not isinstance(post_data['start'], int):
            return False
        if 'end' not in post_data or not isinstance(post_data['end'], int):
            return False

        return True

    def crawl(self, post_data):
        """
        Create an instance of DataCrawler and run the crawler

        :param post_data: Object containing parameters for creating a
        DataCrawler instance
        :return sentiments: A dictionary containing the fields 'word',
        'timestamps', 'score', 'vote', and 'frequency'. 'word' is string, 'frequency' is
        an integer, 'timestamps' is a list of integers of size 'frequency',
        'vote' is a list of integers of size 'frequency' and
        'score' is a list of floats of size 'frequency'.
        """
        crawler = DataCrawler(post_data)
        sentiments = crawler.run()
        return sentiments

    def send_words(self, sentiments):
        """
        Send frequencies response to WordCloud module

        :param freqs: A list of tuples containing filtered words and
        frequencies.
        :param sentiments: A dictionary containing the fields 'word',
        'timestamps', 'score', 'vote', and 'frequency'. 'word' is string, 'frequency' is
        an integer, 'timestamps' is a list of integers of size 'frequency',
        'vote' is a list of integers of size 'frequency' and
        'score' is a list of floats of size 'frequency'.
        :return: Returns none
        """

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        json_data = json.dumps(sentiments).encode('utf-8')
        self.wfile.write(json_data)

    def do_POST(self):
        """
        Handle a POST request. This method is inherited from
        BaseHTTPRequestHandler.

        :return: Returns none
        """
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length).decode('utf-8'))

        if self.validated(post_data):
            sentiments = self.crawl(post_data)
            self.send_words(sentiments)
        else:
            self.send_error(400, 'Invalid parameters supplied')

    def do_OPTIONS(self):
        """
        Set options for requests to enable Cross Origin Requests (CORS). This method is inherited from
        BaseHTTPRequestHandler.

        :return: Returns none
        """
        self.send_response(200, 'ok')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    port = 8080
    print('Listening on localhost:%s' % port)
    server = HTTPServer(('', port), RequestHandler)
    server.serve_forever()

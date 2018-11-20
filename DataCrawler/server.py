"""
The RequestHandler module serves POST requests to fetch frequencies and
comments from the DataCrawler class and forwards the results to the WordCloud
and SentimentAnalyzer modules.
"""
import json, http.client
from functools import partial
from data_crawler import DataCrawler
from http.server import HTTPServer, BaseHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):
    """
    Encapsulates an instance of the RequestHandler class. This class subclasses
    http.server's BaseHTTPRequestHandler.
    """
    def __init__(self, test, *args, **kwargs):
        """
        Construct a new instance of RequestHandler

        :param test: Boolean of whether or not we are testing (to set the client
        endpoint and port)
        :param: Client endpoint
        :param: Client port
        :return: Returns none
        """
        if test:
            self.client_endpoint = '127.0.0.1'
            self.client_port = 8081
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
        :return freq, comments: A list of tuples containing filtered words and
        frequencies and a list of tuples containing individual comments
        and upvotes.
        """
        crawler = DataCrawler(post_data)
        freqs, comments = crawler.run()
        return freqs, comments

    def send_freqs(self, freqs):
        """
        Send frequencies response to WordCloud module

        :param freq: A list of tuples containing filtered words and
        frequencies.
        :return: Returns none
        """
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        data = json.dumps(freqs).encode('utf-8')
        self.wfile.write(data)

    def send_comments(self, comments):
        """
        Send comments to SentimentModel module

        :param comments: A list of tuples containing individual comments
        and upvotes.
        :return: Returns none
        """
        connection = http.client.HTTPConnection(self.client_endpoint,
                port=self.client_port)
        headers = {'Content-type': 'application/json'}
        json_words = json.dumps(comments)
        connection.request('POST', '/', json_words, headers)
        response = connection.getresponse()
        if response.status!=200:
            print('Client server down')

    def do_POST(self):
        """
        Handle a POST request. This method is inherited from
        BaseHTTPRequestHandler.

        :return: Returns none
        """
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length).decode('utf-8'))

        if self.validated(post_data):
            freqs, comments = self.crawl(post_data)
            self.send_freqs(freqs)
            self.send_comments(comments)
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
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
if __name__ == '__main__':
    port = 8080
    print('Listening on localhost:%s' % port)
    handler = partial(RequestHandler, True)
    server = HTTPServer(('', port), handler)
    server.serve_forever()

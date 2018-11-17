import json, http.client
from functools import partial
from constants import SENTIMENT_ANALYZER_ENDPOINT
from data_crawler import DataCrawler
from http.server import HTTPServer, BaseHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, test, *args, **kwargs):
        if test:
            self.client_endpoint = '127.0.0.1'
            self.client_port = 8081
        super().__init__(*args, **kwargs)

    def validated(self, post_data):
        if 'subreddit' not in post_data or not isinstance(post_data['subreddit'], str):
            return False
        if 'start' not in post_data or not isinstance(post_data['start'], int):
            return False
        if 'end' not in post_data or not isinstance(post_data['end'], int):
            return False

        return True

    def crawl(self, post_data):
        crawler = DataCrawler(post_data)
        freqs, comments = crawler.run()
        return freqs, comments

    def send_freqs(self, freqs):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        data = json.dumps(freqs).encode('utf-8')
        self.wfile.write(data)

    def send_comments(self, comments):
        connection = http.client.HTTPConnection(self.client_endpoint,
                port=self.client_port)
        headers = {'Content-type': 'application/json'}
        json_words = json.dumps(comments)
        connection.request('POST', '/', json_words, headers)
        response = connection.getresponse()
        if response.status!=200:
            print('Client server down')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length).decode('utf-8'))

        if self.validated(post_data):
            freqs, comments = self.crawl(post_data)
            self.send_freqs(freqs)
            self.send_comments(comments)
        else:
            self.send_error(400, 'Invalid parameters supplied')

    def do_OPTIONS(self):
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

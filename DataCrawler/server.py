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

    def _crawl(self, post_data):
        crawler = DataCrawler(post_data)
        freq = crawler.run()
        return freq

    def send_freq(self, freq):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        data = json.dumps(freq).encode('utf-8')
        self.wfile.write(data)

    def send_words(self, freq):
        words = [i[0] for i in freq]
        connection = http.client.HTTPConnection(self.client_endpoint,
                port=self.client_port)
        headers = {'Content-type': 'application/json'}
        json_words = json.dumps(words)
        connection.request('POST', '/', json_words, headers)
        response = connection.getresponse()
        if response.status!=200:
            print('Client server down')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length).decode('utf-8'))

        if self.validated(post_data):
            freq = self._crawl(post_data)
            self.send_freq(freq)
            self.send_words(freq)
        else:
            self.send_error(400, 'Invalid parameters supplied')
        
if __name__ == "__main__":
    port = 8080
    print('Listening on localhost:%s' % port)
    handler = partial(RequestHandler, True)
    server = HTTPServer(('', port), handler)
    server.serve_forever()

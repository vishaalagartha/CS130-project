import json, http.client
from constants import SENTIMENT_ANALYZER_ENDPOINT
from data_crawler2 import DataCrawler
from http.server import HTTPServer, BaseHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):
    def _validated(self, post_data):
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

    def _send_freqs(self, freq):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        data = json.dumps(freq).encode('utf-8')
        self.wfile.write(data)

    def _send_words(self, freq):
        words = [i[0] for i in freq]
        connection = http.client.HTTPSConnection(SENTIMENT_ANALYZER_ENDPOINT)
        headers = {'Content-type': 'application/json'}
        json_words = json.dumps(words)
        connection.request('POST', '/', json_words, headers)
        response = connection.getresponse()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length).decode('utf-8'))

        if self._validated(post_data):
            freq = self._crawl(post_data)
            self._send_freqs(freq)
            #self._send_words(freq)
        else:
            self.send_error(400, 'Invalid parameters supplied')
        
        
port = 8080
print('Listening on localhost:%s' % port)
server = HTTPServer(('', port), RequestHandler)
server.serve_forever()


from http.server import HTTPServer, BaseHTTPRequestHandler

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Data_Analysis_Toolkit LIVE")

HTTPServer(("0.0.0.0",8080),H).serve_forever()

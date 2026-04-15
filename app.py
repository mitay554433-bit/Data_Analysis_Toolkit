import os
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", 8080))

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Data Analysis Toolkit LIVE")

HTTPServer(("0.0.0.0", PORT), H).serve_forever()

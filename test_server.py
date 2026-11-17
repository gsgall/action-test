from http.server import BaseHTTPRequestHandler, HTTPServer

MESSAGE = b"Hello from the test server!\n"


from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def reply(self, message):
        body = message.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self.reply(f"GET received for path {self.path}\n")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(length).decode()
        self.reply(f"POST received with {length} bytes: {data}\n")


print("Listening on http://localhost:8000")
HTTPServer(("", 8000), Handler).serve_forever()

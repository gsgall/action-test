import functools
import hashlib
import hmac
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

# this will make the url publically available
# ssh -R 80:localhost:8000 nokey@localhost.run

print = functools.partial(print, flush=True)  # show output immediately
with open(".env") as f:
    SECRET = f.read().strip().encode()

print(SECRET)


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        print("=" * 60)
        print("Event:   ", self.headers.get("X-GitHub-Event"))
        print("Delivery:", self.headers.get("X-GitHub-Delivery"))
        try:
            print(json.dumps(json.loads(body), indent=2))
        except ValueError:
            print(body.decode(errors="replace"))
        self.send_response(200)
        expected = "sha256=" + hmac.new(SECRET, body, hashlib.sha256).hexdigest()
        received = self.headers.get("X-Hub-Signature-256", "")
        if not hmac.compare_digest(expected, received):
            print("Bad signature, rejecting")
            self.send_response(401)
            self.end_headers()
            return self.end_headers()


print("Waiting for webhooks on port 8000...")
HTTPServer(("", 8000), Handler).serve_forever()

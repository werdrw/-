from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import urllib.error
import json
import os

API_KEY  = "sk-SCZUYySlDfvTNl0yU4eLzQ"
API_URL  = "https://elmodels.ngrok.app/v1/chat/completions"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class Handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self._cors()

    def do_GET(self):
        path = "index.html" if self.path in ("/", "/index.html") else self.path.lstrip("/")
        full = os.path.join(ROOT_DIR, path)
        if os.path.isfile(full):
            with open(full, "rb") as f:
                content = f.read()
            ctype = "text/html; charset=utf-8" if full.endswith(".html") else "text/plain"
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self._cors()
            self.wfile.write(content)
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path != "/api/chat":
            self.send_error(404)
            return

        length = int(self.headers.get("Content-Length", 0))
        body   = self.rfile.read(length)

        try:
            req = urllib.request.Request(
                API_URL,
                data=body,
                headers={
                    "Content-Type":  "application/json",
                    "Authorization": f"Bearer {API_KEY}"
                }
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = resp.read()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._cors()
            self.wfile.write(result)

        except urllib.error.HTTPError as e:
            err = json.dumps({"error": str(e)}).encode()
            self.send_response(e.code)
            self.send_header("Content-Type", "application/json")
            self._cors()
            self.wfile.write(err)

        except Exception as e:
            err = json.dumps({"error": str(e)}).encode()
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self._cors()
            self.wfile.write(err)

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin",  "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def log_message(self, fmt, *args):
        print(f"  {args[0]}  {args[1]}")

if __name__ == "__main__":
    port   = 8080
    import socket
    local_ip = socket.gethostbyname(socket.gethostname())
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"\n  على جهازك:        http://localhost:{port}")
    print(f"  للأجهزة الثانية:  http://{local_ip}:{port}\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  تم إيقاف السيرفر.")

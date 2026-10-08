import http.server
import socketserver
import os
import json
import urllib.parse
# pyrefly: ignore [missing-import]
from langchain_backend import langchain_engine

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class PortfolioHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Enable CORS and disable caching for instant updates
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def _send_json(self, data: dict, status_code: int = 200):
        response_bytes = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(response_bytes)))
        self.end_headers()
        self.wfile.write(response_bytes)

    def _read_json_body(self) -> dict:
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length <= 0:
            return {}
        raw_body = self.rfile.read(content_length).decode('utf-8')
        try:
            return json.loads(raw_body)
        except json.JSONDecodeError:
            return {}

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # Status endpoint
        if path in ['/api/status', '/api/ai-status']:
            self._send_json({
                "status": "online",
                "model": "LangChain v1.3.0 RAG Chain",
                "assistant": "Gagan AI Assistant"
            })
            return

        # Default static file handling
        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # LangChain Conversation API
        if path in ['/api/chat', '/api/conversation']:
            payload = self._read_json_body()
            user_message = payload.get('message', '')
            history = payload.get('history', [])

            result = langchain_engine.generate_response(user_message, history)
            self._send_json(result)
            return

        self._send_json({"error": "Endpoint not found"}, status_code=404)

if __name__ == '__main__':
    os.chdir(DIRECTORY)
    # Allow address reuse
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), PortfolioHTTPHandler) as httpd:
        print(f"Serving Gagandeep Kaur Portfolio with LangChain API at http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()

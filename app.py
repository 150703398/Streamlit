#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.server
import socketserver
import urllib.parse
import threading
import os
import json
import base64
import uuid
from pathlib import Path

INSTALL_DIR = Path.home() / ".agsb"
INSTALL_DIR.mkdir(exist_ok=True)

SUB_TOKEN_FILE = INSTALL_DIR / "sub_token.txt"
NODES_FILE = INSTALL_DIR / "allnodes.txt"

DEFAULT_SUB_TOKEN = "sub"

# ================== Token ==================
if not SUB_TOKEN_FILE.exists():
    SUB_TOKEN_FILE.write_text(DEFAULT_SUB_TOKEN)

SUB_TOKEN = SUB_TOKEN_FILE.read_text().strip()

# ================== 伪装测速网站 ==================
SPEEDTEST_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Network Speed Test</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font-family:Arial;background:#0f172a;color:#e5e7eb;text-align:center;padding:40px}
.card{max-width:480px;margin:auto;background:#020617;padding:30px;border-radius:12px}
button{padding:12px 20px;font-size:16px;border:none;border-radius:8px;background:#38bdf8}
</style>
</head>
<body>
<div class="card">
<h1>Network Speed Test</h1>
<p>Test your internet speed easily</p>
<button onclick="test()">Start Test</button>
<p id="result"></p>
</div>
<script>
function test(){
 document.getElementById("result").innerText =
 "Download: " + (50+Math.random()*150).toFixed(2) + " Mbps | " +
 "Upload: " + (20+Math.random()*80).toFixed(2) + " Mbps";
}
</script>
</body>
</html>
"""

# ================== HTTP Server ==================
class Handler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        # ===== 订阅接口 =====
        if parsed.path == "/sub":
            qs = urllib.parse.parse_qs(parsed.query)
            token = qs.get("token", [""])[0]

            if token != SUB_TOKEN:
                self.fake_site()
                return

            if not NODES_FILE.exists():
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"No subscription")
                return

            data = NODES_FILE.read_text()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(data.encode())
            return

        # ===== 其他路径 → 伪装网站 =====
        self.fake_site()

    def fake_site(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(SPEEDTEST_HTML.encode())

    def log_message(self, *args):
        return


# ================== 启动 HTTP ==================
def start_http(port):
    with socketserver.TCPServer(("127.0.0.1", port), Handler) as httpd:
        httpd.serve_forever()


if __name__ == "__main__":
    port = 18080
    print(f"[+] Fake website & subscription server on 127.0.0.1:{port}")
    print(f"[+] Subscription: /sub?token={SUB_TOKEN}")
    start_http(port)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.server
import socketserver
import urllib.parse
import threading
import os
import json
import base64
import uuid
from pathlib import Path

INSTALL_DIR = Path.home() / ".agsb"
INSTALL_DIR.mkdir(exist_ok=True)

SUB_TOKEN_FILE = INSTALL_DIR / "sub_token.txt"
NODES_FILE = INSTALL_DIR / "allnodes.txt"

DEFAULT_SUB_TOKEN = "sub"

# ================== Token ==================
if not SUB_TOKEN_FILE.exists():
    SUB_TOKEN_FILE.write_text(DEFAULT_SUB_TOKEN)

SUB_TOKEN = SUB_TOKEN_FILE.read_text().strip()

# ================== 伪装测速网站 ==================
SPEEDTEST_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Network Speed Test</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font-family:Arial;background:#0f172a;color:#e5e7eb;text-align:center;padding:40px}
.card{max-width:480px;margin:auto;background:#020617;padding:30px;border-radius:12px}
button{padding:12px 20px;font-size:16px;border:none;border-radius:8px;background:#38bdf8}
</style>
</head>
<body>
<div class="card">
<h1>Network Speed Test</h1>
<p>Test your internet speed easily</p>
<button onclick="test()">Start Test</button>
<p id="result"></p>
</div>
<script>
function test(){
 document.getElementById("result").innerText =
 "Download: " + (50+Math.random()*150).toFixed(2) + " Mbps | " +
 "Upload: " + (20+Math.random()*80).toFixed(2) + " Mbps";
}
</script>
</body>
</html>
"""

# ================== HTTP Server ==================
class Handler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        # ===== 订阅接口 =====
        if parsed.path == "/sub":
            qs = urllib.parse.parse_qs(parsed.query)
            token = qs.get("token", [""])[0]

            if token != SUB_TOKEN:
                self.fake_site()
                return

            if not NODES_FILE.exists():
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"No subscription")
                return

            data = NODES_FILE.read_text()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(data.encode())
            return

        # ===== 其他路径 → 伪装网站 =====
        self.fake_site()

    def fake_site(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(SPEEDTEST_HTML.encode())

    def log_message(self, *args):
        return


# ================== 启动 HTTP ==================
def start_http(port):
    with socketserver.TCPServer(("127.0.0.1", port), Handler) as httpd:
        httpd.serve_forever()


if __name__ == "__main__":
    port = 18080
    print(f"[+] Fake website & subscription server on 127.0.0.1:{port}")
    print(f"[+] Subscription: /sub?token={SUB_TOKEN}")
    start_http(port)

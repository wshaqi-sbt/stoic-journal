"""One-time OAuth login: opens browser, catches redirect, saves tokens.json."""
import json
import os
import secrets
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlencode, urlparse

import requests
from dotenv import load_dotenv

AUTH_URL = "https://api.prod.whoop.com/oauth/oauth2/auth"
TOKEN_URL = "https://api.prod.whoop.com/oauth/oauth2/token"
SCOPES = "read:recovery read:sleep read:cycles read:workout read:body_measurement offline"

load_dotenv()
client_id = os.environ["WHOOP_CLIENT_ID"]
client_secret = os.environ["WHOOP_CLIENT_SECRET"]
redirect_uri = os.environ["WHOOP_REDIRECT_URI"]

state = secrets.token_urlsafe(16)
auth_params = {
    "response_type": "code",
    "client_id": client_id,
    "redirect_uri": redirect_uri,
    "scope": SCOPES,
    "state": state,
}
received = {}


class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        qs = parse_qs(urlparse(self.path).query)
        received["code"] = qs.get("code", [None])[0]
        received["state"] = qs.get("state", [None])[0]
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write("Logged in, you can close this tab.".encode("utf-8"))

    def log_message(self, *args):
        pass


port = urlparse(redirect_uri).port or 8000

server = HTTPServer(("localhost", port), CallbackHandler)
webbrowser.open(f"{AUTH_URL}?{urlencode(auth_params)}")
print("Waiting for authorization in the browser...")
while "code" not in received:
    server.handle_request()

if received["state"] != state:
    raise SystemExit("State mismatch, possible CSRF, aborted.")

resp = requests.post(
    TOKEN_URL,
    data={
        "grant_type": "authorization_code",
        "code": received["code"],
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
    },
)
resp.raise_for_status()
tokens = resp.json()
tokens["obtained_at"] = int(time.time())

with open("tokens.json", "w") as f:
    json.dump(tokens, f, indent=2)

print("Saved tokens.json")

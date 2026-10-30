"""Whoop API v2 client: token refresh."""
import json
import os
import time

import requests
from dotenv import load_dotenv

TOKEN_URL = "https://api.prod.whoop.com/oauth/oauth2/token"
API_BASE = "https://api.prod.whoop.com/developer/v2"

load_dotenv()


def _load_tokens():
    with open("tokens.json") as f:
        return json.load(f)


def _save_tokens(tokens):
    with open("tokens.json", "w") as f:
        json.dump(tokens, f, indent=2)


def get_access_token():
    tokens = _load_tokens()

    expires_at = tokens["obtained_at"] + tokens["expires_in"]
    if time.time() < expires_at - 60:
        return tokens["access_token"]

    resp = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "refresh_token",
            "refresh_token": tokens["refresh_token"],
            "client_id": os.environ["WHOOP_CLIENT_ID"],
            "client_secret": os.environ["WHOOP_CLIENT_SECRET"],
        },
    )
    resp.raise_for_status()
    new_tokens = resp.json()
    new_tokens["obtained_at"] = int(time.time())
    _save_tokens(new_tokens)
    return new_tokens["access_token"]

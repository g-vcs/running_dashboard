import json
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

TOKENS_PATH = Path("tokens.json")
CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
URL = "https://www.strava.com/oauth/token"


def load_tokens():
    """Read file tokens.json and return a dictionary with tokens."""
    with TOKENS_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def save_tokens(tokens):
    """Save the dictionary of tokens in tokens.json file."""
    with TOKENS_PATH.open("w", encoding="utf-8") as f:
        json.dump(tokens, f)


def refresh_access_token():
    """Uses the refresh_tokens to get a new access_token in Strava"""
    tokens = load_tokens()
    refresh_token = tokens["refresh_token"]

    response = requests.post(
        URL,
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        },
        timeout=10
    )

    response.raise_for_status()
    data = response.json()
    tokens["access_token"] = data["access_token"]
    tokens["expires_at"] = data["expires_at"]
    tokens["refresh_token"] = data.get("refresh_token", refresh_token)

    save_tokens(tokens)
    return tokens


def get_valid_access_token():
    tokens = load_tokens()
    now = int(time.time())

    if tokens.get("expires_at") is not None and tokens["expires_at"] <= now + 300:
        tokens = refresh_access_token()

    return tokens["access_token"]


if __name__ == "__main__":
    print("Tokens antes do refresh:", load_tokens())
    tokens = refresh_access_token()
    print("Novo access token:", tokens["access_token"])
    print("Tokens depois do refresh:", load_tokens())

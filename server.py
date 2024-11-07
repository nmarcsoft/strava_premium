#!/home/nicolas/Documents/perso/strava_prenium/.venv/bin/python

from os import access
import requests
from pprint import pprint
from flask import Flask, request, redirect, jsonify
import json

from API_manager import API_manager

app = Flask(__name__)

with open('credentials.json', 'r') as f:
    credentials = json.load(f)
    client_id = credentials.get("client_id")
    client_secret = credentials.get("client_secret")
    redirect_uri = "http://localhost:8000/callback"


@app.route('/')
def home():
    auth_url = (
        f"https://www.strava.com/oauth/authorize?"
        f"client_id={client_id}&"
        f"response_type=code&"
        f"redirect_uri={redirect_uri}&"
        f"approval_prompt=force&"
        f"scope=activity:read_all"
    )
    return redirect(auth_url)


@app.route('/callback')
def callback():
    auth_code = request.args.get("code")
    if not auth_code:
        return "Authorization failed: no code provided", 400

    access_token = get_access_token(auth_code)
    if access_token:
        manager = API_manager(access_token)
        manager.get_all_activities()
        print(manager.activites)
        return "Activity created successfully! Check your Strava account."
    else:
        return "Failed to retrieve access token", 500


def get_access_token(auth_code):
    token_url = "https://www.strava.com/oauth/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": auth_code,
        "grant_type": "authorization_code"
    }
    response = requests.post(token_url, data=payload)
    response.raise_for_status()
    access_token = response.json().get("access_token")
    print(f"access_token: {access_token}")
    return access_token




if __name__ == '__main__':
    app.run(port=8000)

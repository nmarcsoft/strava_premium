import requests
from pprint import pprint
from flask import Flask, request, redirect, jsonify
import json

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
        f"scope=activity:write"
    )
    return redirect(auth_url)

@app.route('/callback')
def callback():
    auth_code = request.args.get("code")
    if not auth_code:
        return "Authorization failed: no code provided", 400

    access_token = get_access_token(auth_code)
    if access_token:
        create_activity(access_token)
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
    return access_token

def create_activity(access_token):
    url = "https://www.strava.com/api/v3/activities"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    activity_data = {
        "name": "Sample Activity",
        "sport_type": "Run",
        "start_date_local": "2013-10-20T19:20:30+01:00",
        "elapsed_time": 56,
        "type": "Run",
        "description": "Morning run",
        "distance": 3400,
        "trainer": 1,
        "commute": 1
    }

    try:
        response = requests.post(url, headers=headers, json=activity_data)
        response.raise_for_status()
        pprint(response.json())
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    app.run(port=8000)


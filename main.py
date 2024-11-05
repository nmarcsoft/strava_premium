#!/.venv/bin/python3

import requests
import json
from pprint import pprint

with open('credentials.json', 'r') as f:
    credentials = json.load(f)
    client_id = credentials.get("client_id")
    client_secret = credentials.get("client_secret")
    redirect_uri = credentials.get("redirect_uri")

def get_authorization_url():
    auth_url = (
        f"https://www.strava.com/oauth/authorize?"
        f"client_id={client_id}&"
        f"response_type=code&"
        f"redirect_uri={redirect_uri}&"
        f"approval_prompt=force&"
        f"scope=activity:write"
    )
    print("Go to the following URL to authorize the app:")
    print(auth_url)

get_authorization_url()

import os
import time
import sqlite3
from flask import Flask, request, render_template, redirect
import requests
from requests.exceptions import ConnectionError, HTTPError

app = Flask(__name__)

CLIENT_ID = 166896
CLIENT_SECRET = '0a73b7f372be641908e23d6b72dc76f9cbd5430f'
REDIRECT_URI = 'https://strava-api-06ge.onrender.com/strava_callback'


@app.route("/")
def index():
    return render_template("index.html", greeting="Hello and welcome!")

@app.route("/authorization", methods=["POST"])
def authorization():
    return redirect("https://www.strava.com/oauth/authorize?client_id=166896&response_type=code&redirect_uri=https://strava-api-06ge.onrender.com/strava_callback&approval_prompt=force&scope=read")

@app.route("/strava_callback")
def strava_callback():
    code = request.args.get("code")
    if not code:
        return render_template("failure.html", message="could not obtain code")
    try:
        token = requests.post("https://www.strava.com/oauth/token", data={
                        'client_id': 166896,
                'client_secret': '0a73b7f372be641908e23d6b72dc76f9cbd5430f',
                'code': code,
                'grant_type': 'authorization_code'
                
    }, headers={'Accept': 'application/json'})
        token.raise_for_status()
    except ConnectionError as conErr:
        return render_template('failure.html', message=conErr)
    except HTTPError as httpErr:
        error_code = token.status_code
        return render_template("failure.html", message=f"{httpErr} with error code {error_code}")

    token_decoded = token.json()
    access_token = token_decoded["access_token"]
    if not access_token:
        return render_template("failure.html", message="failed to get access token")
    athlete_username = token_decoded["athlete"]["username"]
    athlete_id = token_decoded["athlete"]["id"]
    return render_template("information.html", athlete_username=athlete_username, athlete_id=athlete_id)

def get_refresh_token()
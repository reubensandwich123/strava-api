import os
from flask import Flask, request, render_template, redirect, session
from flask_session import Session
import requests
from requests.exceptions import ConnectionError, HTTPError
import time

app = Flask(__name__)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
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
                        'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'code': code,
                'grant_type': 'authorization_code', 
                'redirect_uri' : REDIRECT_URI
                
    }, headers={'Accept': 'application/json'})
        token.raise_for_status()
    except ConnectionError as conErr:
        return render_template('failure.html', message=conErr)
    except HTTPError as httpErr:
        error_code = token.status_code
        return render_template("failure.html", message=f"{httpErr} with error code {error_code}")

    token_decoded = token.json()
    session["access_token"] = token_decoded["access_token"]
    session["expires_at"] = token_decoded["expires_at"]
    session["refresh_token"] = token_decoded["refresh_token"]
    session["expires_in"] = token_decoded["expires_in"]
    if not token_decoded["access_token"]:
        return render_template("failure.html", message="failed to get access token")
    session["athlete_username"] = token_decoded["athlete"]["username"]
    session["athlete_id"] = token_decoded["athlete"]["id"]
    return render_template("information.html", athlete_username=session["athlete_username"], athlete_id=session["athlete_id"])


@app.route("/stats", methods=["POST"])
def stats():
    result = check_expiry(session["expires_at"])
    if (result == True):

        id = session["athlete_id"]
        token = session["access_token"]
        try:
            response = requests.get(f"https://www.strava.com/api/v3/athletes/{id}/stats", headers={"Authorization": f"Bearer {token}"})
            response.raise_for_status()
        except ConnectionError as connErr:
            return render_template("failure.html", message=str(connErr)
        except HTTPError as httpErr:
            status = response.status_code
            return render_template('failure.html', message=f"{httpErr} with error code {status}")
        response = response.json()
        run_totals = response["all_run_totals"]
        ride_totals = response["all_ride_totals"]
        swim_totals = response["all_swim_totals"]
        return render_template('stats.html', run_total=run_totals, ride_total=ride_totals, swim_total=swim_totals)
    else:
        return render_template("failure.html", message=(str(result)))
def check_expiry(expires_at):
    refresh_token = session["refresh_token"]
    if (expires_at < time.time()):
        res = refresh(refresh_token)
        if (res != 0):
            return res
        else:
            return True
    else:
        return True
        
def refresh(refresh_token):
    try: 
        response = requests.post("https://www.strava.com/oauth/token", data={            
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token}, headers={'Accept' : 'application/json'})
        response.raise_for_status()
    except ConnectionError as connErr:
        return str(connErr)
    except HTTPError as httpErr:
        status_code = response.status_code
        message=f"{httpErr} with error code {status_code}"
        return message
        
    response = response.json()
    session["access_token"] = response["access_token"]
    session["refresh_token"] = response["refresh_token"]
    session["expires_at"] = response["expires_at"]
    session["expires_in"] = response["expires_in"]
    return 0
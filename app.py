from flask import Flask, request, render_template
import requests
from requests.exceptions import ConnectionError, HTTPError

app = Flask(__name__)










@app.route("/")
def index():
    return render_template("index.html", greeting="Hello and welcome!")

@app.route("/auth_callback_dmain")
def auth_callback():
    return render_template("auth_callback_domain.html")
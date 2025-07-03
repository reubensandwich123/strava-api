from flask import Flask, request, render_template
import requests
from requests.exceptions import ConnectionError, HTTPError

app = Flask(__name__)










@app.route("/")
def index():
    return render_template("index.html", greeting="Hello and welcome!")


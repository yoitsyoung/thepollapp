import os

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from models import *


import requests
import logging



app = Flask(__name__)

@app.route("/")
def index():
    return render_template("client.html")
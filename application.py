import os, requests, logging

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL_POLLAPP")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)



@app.route("/")
def index():
    return render_template("client.html")

#api to get a question, with options
@app.route("/api/<int:question_id>")
def get_question(question_id):
    #get question information using question id, converted to dict then to json format
    question_count = 1
    question = Question.query.get(question_id)
    if not question:
        return ('Error, question does not exist')

    response = {}
    response['Success'] = 'True'

    #Integer 1 represents 1st question instance, in case we want to request multiple questions in future
    response[question_count] = {
                "question_id": question.id,
                "text": question.title,
                "date": question.date,
                "questions": {}
    }

    #create dictionary for each option. Will nest within questions dictionary
    option_count =  0
    for option in question.options:
        option_dict = {
                "option_id":option.id,
                "text":option.title,
                "img":option.img,
                "score":option.score
        }
        response[question_count]['questions'][option_count] = option_dict
        option_count += 1
    
    return jsonify(response)

#receive new question. Expecting a dataset of similar structure, and terms to api
@app.route("add_question", methods = ['POST'])
def add_question():
    data = request.form
        
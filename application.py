import os, requests, logging

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL_POLLAPP")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

#a route to reload the database. should remove before production
@app.route('/load_db')
def load_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        return ('Databse reloaded')

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
                "options": {}
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
        response[question_count]['options'][option_count] = option_dict
        option_count += 1
    
    return jsonify(response)

#receive new question. Expecting a dataset of similar structure, and terms to api, but there is only one question
@app.route("/add_question", methods = ['POST'])
def add_question():
    data = request.form
    app.logger.info("Received qn post...")
    app.logger.info(data)
    qn_title = data[0]['text']
    options_dict = data[0]['options']
    question = Question(title=qn_title)
    for option in options_dict.values():
        title = option['text']
        img = option['img']
        question.add_option(title=title, img=img)
    db.session.add(question)
    db.commit()


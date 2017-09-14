import os
import flask
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy

app=flask.Flask(__name__)


""" I will need three routes,
a GET (for retrieve all)
a POST (for create new item)
a PUT (for mark item as complete) """
@app.route('/', methods=["GET"])
def show_all():
    # will return all items in todo list
    return 'Hello, World!'

@app.route('/new', methods=["POST"])
def add_item():
    # will add new item to db

@app.route('/comp/<int:id>', methods=["PUT"])
def mark_complete():
    #will update an item's complete feild to trueflask

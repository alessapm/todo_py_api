import os
import flask
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.orm import column_property
from sqlalchemy.ext.declarative import declarative_base

app=flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/todo_tictail'
db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = 'todo_list'

    id = db.Column(db.Integer, primary_key=True)
    item = Column(db.String(500))
    completed = Column(db.Boolean)


""" I will need three routes,
a GET (for retrieve all)
a POST (for create new item)
a PUT (for mark item as complete) """
@app.route('/', methods=["GET"])

def show_all():
    # will return all items in todo list
    print "inside show_all"
    data = db.session.query('todo_list').all()
    return data

@app.route('/new', methods=["POST"])
# print "request: " + request
def add_item():
    # will add new item to db
    db.query('INSERT INTO todo_list (item, highlight, completed) values (?, ?)',
                 [request.form['item'], request.form['highlight'], request.form['completed']])
    # db.commit()

    # return data somehow?

@app.route('/comp/<int:id>', methods=["PUT"])
def mark_complete():
    #will update an item's complete feild to trueflask
    return db.query('SELECT * FROM todo_list')

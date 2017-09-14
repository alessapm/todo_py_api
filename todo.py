import os
import flask
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy

app=flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/todo_tictail'
db = SQLAlchemy(app)


""" I will need three routes,
a GET (for retrieve all)
a POST (for create new item)
a PUT (for mark item as complete) """
@app.route('/', methods=["GET"])

def show_all():
    # will return all items in todo list
    return db.execute('SELECT * FROM todo_list')

@app.route('/new', methods=["POST"])
print "request: " + request
def add_item():
    # will add new item to db
    db.execute('INSERT INTO todo_list (item, highlight, completed) values (?, ?)',
                 [request.form['item'], request.form['highlight'], request.form['completed']])
    db.commit()

    # return data somehow?

@app.route('/comp/<int:id>', methods=["PUT"])
def mark_complete():
    #will update an item's complete feild to trueflask

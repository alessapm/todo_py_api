
import flask
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy import Column, Integer, String, ForeignKey
from flask_cors import CORS

from flask import jsonify


app=flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# create table todo_list(id integer primary key autoincrement,item text, completed boolean);

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
    data = Todo.query.all()

    print data
    return jsonify({'todo': data});

@app.route('/new', methods=["POST", "GET"])
# print "request: " + request
def add_item():
    # will add new item to db
    if flask.request.method=="POST":
        return db.session.query('INSERT INTO todo_list (item, highlight, completed) values (?, ?)',
                 [request.form['item'], request.form['highlight'], request.form['completed']])

    # db.commit()
    if flask.request.method=="GET":
        insert = 'INSERT INTO todo_list (item, completed) values ("go to the gym", false);'
        db.session.query(insert)

    # return data somehow?

# @app.route('/comp/<int:id>', methods=["PUT"])
#     # has to pass an id to mark_complete
# def mark_complete(id):
#     #will update an item's complete feild to true
#     return db.session.query('UPDATE complete = true in todo_list where id = ? ', id)


# do i need this?
app.run()

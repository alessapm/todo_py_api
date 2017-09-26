
import flask
from flask import request
from flask_sqlalchemy  import SQLAlchemy

from sqlalchemy import Column, Integer, String, ForeignKey
from flask_cors import CORS

from flask import jsonify


app=flask.Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# do i need this?
app.config['SQLALCHEMY_ECHO'] = True

# create table todo_list(id integer primary key autoincrement,item text, completed boolean);

class Todo(db.Model):
    __tablename__ = 'todo_list'

    id = db.Column(db.Integer, primary_key=True)
    item = Column(db.String(500))
    completed = Column(db.Boolean)

    def to_json(this):
        return  {'id' : this.id, 'item': this.item, 'completed': this.completed}

""" I will need three routes,
a GET (for retrieve all)
a POST (for create new item)
a PUT (for mark item as complete) """
@app.route('/todo', methods=["GET"])

def show_all():
    # will return all items in todo list
    print "inside show_all"
    data = Todo.query.all()

    result_list = []
    for result in data:
        result_list.append(result.to_json())

    return jsonify(result_list)

@app.route('/todo/new', methods=["POST"])
# print "request: " + request
def add_item():
    print request.args

    if 'item' not in request.args:
        return jsonify({ 'message':'Error: Missing Item'})

    if 'completed' not in request.args:
        completed = False
    else:
        completed = request.args.get('completed')

#populate model object
    todo = Todo()
    todo.item = request.args.get('item')
    todo.completed = completed

# saves obj and commits it
    db.session.add(todo)
    db.session.commit()

    return jsonify(todo.to_json())



@app.route('/todo/complete/<int:id>', methods=["PUT"])
    # has to pass an id to mark_complete
def mark_complete(id):
    print 'id: ' + str(id)

    todo = Todo.query.get(id)

    todo.completed = not todo.completed
    db.session.commit()

    return jsonify(todo.to_json())


@app.route('/todo/complete/all', methods=["PUT"])

def mark_all_complete():
    all_results = Todo.query.all()

    for result in all_results:
        result.completed = True
    db.session.commit()

    return 'completed'

@app.route('/todo/destroy/<int:id>', methods=["DELETE"])

def delete_item(id):
    item = Todo.query.get(id)

    db.session.delete(item)
    db.session.commit()

    return 'delete completed'

app.run()

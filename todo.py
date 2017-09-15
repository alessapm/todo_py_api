from flask import Flask, request, jsonify
from flask_sqlalchemy  import SQLAlchemy


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/todo_tictail'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_RECORD_QUERIES'] = True  ##comment me out to stop debugging
app.config['SQLALCHEMY_ECHO'] = True            ##comment me out to stop debugging

# initialize SQLAlchemy
db = SQLAlchemy(app)

#create statement for sqlite
#create table todo_list(id integer primary key autoincrement,item text, completed boolean);

#declare model
class Todo(db.Model):
    __tablename__ = 'todo_list'

    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(500))
    completed = db.Column(db.Boolean)

    def __repr__(self):   #use to debug program with print statements
        return '<TODO %d, %r, %d>' % (self.id, self.item, self.completed)

    def to_json(self):    #use to create json from this object
        return  {'id' : self.id, 'item':self.item, 'completed': self.completed}


""" I will need three routes,
a GET (for retrieve all)
a POST (for create new item)
a PUT (for mark item as complete) """


@app.route('/', methods=["GET"])

def show_all():
    # will return all items in todo list
    print "inside show_all"

    #get all of the objects from the database
    results = Todo.query.all()

    #convert each Object to json and load into results_list
    result_list =[]
    for result in results:
        result_list.append(result.to_json())

    #return the list
    return jsonify(result_list)

@app.route('/new', methods=["POST"])

# print "request: " + request
def add_item():
    # will add new item to db

    print request.args

    if 'item' not in request.args:
        return { 'message':'Error: Missing Item'}

    if 'completed' not in request.args:
        completed = False
    else:
        completed = request.args.get('completed')

    # create a populate a new Todo object
    todo = Todo()
    todo.item = request.args.get('item')
    todo.completed = completed

    #save our new Todo object to the database
    db.session.add(todo)
    db.session.commit()

    #return the new object
    return jsonify(todo.to_json())


@app.route('/comp/<int:id>', methods=["PUT"])

# has to pass an id to mark_complete
def mark_complete(id):
    #will update an item's complete feild to true
    print '*****' + str(id) + '****'

    #get this row from database
    todo = Todo.query.get(id)
    if todo is None:
        return { 'message':'Error: Bad Id: ' + id}

    #mark this task as completed and save
    todo.completed = True
    db.session.commit()

    return jsonify(todo.to_json())


# error routes catch 404 and 500 errors
@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'error':True,'message':
        'bad service call - endpoint does not exist'})

@app.errorhandler(500)
def page_server_error(error):
    return jsonify({'error':True,'message': 'internal server error'})


if __name__ == '__main__':
    app.run()

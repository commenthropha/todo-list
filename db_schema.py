from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# create the database interface
db = SQLAlchemy()

# a model of a user for the database
class User(UserMixin, db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.Text())

    def __init__(self, username, password):  
        self.username=username
        self.password=password

# a model of a list for the database
# it refers to a user
class List(db.Model):
    __tablename__='lists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    user_id = db.Column(db.Integer)  # this ought to be a "foreign key"

    def __init__(self, name, user_id):
        self.name=name
        self.user_id = user_id

# a model of a list item for the database
# it refers to a list
class ListItem(db.Model):
    __tablename__='items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    completed = db.Column(db.Boolean())
    list_id = db.Column(db.Integer)  # this ought to be a "foreign key"

    def __init__(self, name, completed, list_id):
        self.name=name
        self.completed = completed
        self.list_id=list_id

# put some data into the tables
def dbinit():
    user_list = [
        User("Anees","ejejekeh2"), 
        User("MajinPhil","P0ln4r3ff")
        ]
    db.session.add_all(user_list)

    anees_id = User.query.filter_by(username="Anees").first().id

    all_lists = [
        List("Shopping",anees_id), 
        List("Chores",anees_id)
        ]
    db.session.add_all(all_lists)

    # find the ids of the lists Chores and Shopping

    chores_id = List.query.filter_by(name="Chores").first().id
    shopping_id= List.query.filter_by(name="Shopping").first().id

    all_items = [
        ListItem("Potatoes", False, shopping_id), 
        ListItem("Shampoo", False, shopping_id),
        ListItem("Wash up", True, chores_id), 
        ListItem("Vacuum bedroom", True, chores_id)
        ]
    db.session.add_all(all_items)

    # commit all the changes to the database file
    db.session.commit()

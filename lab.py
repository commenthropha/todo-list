from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from flask import Flask, render_template
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///todo.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# set up a 'model' for the data you want to store
from db_schema import db, User, List, ListItem, dbinit

# init the database so it can connect with our app
db.init_app(app)

# change this to False to avoid resetting the database every time this app is restarted
resetdb = True
if resetdb:
    with app.app_context():
        # drop everything, create all the tables, then put some data into the tables
        db.drop_all()
        db.create_all()
        dbinit()

#route to the index
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/signup.html')
def signup():
    return render_template('signup.html')


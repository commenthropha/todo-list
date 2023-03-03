from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, current_user, logout_user
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///todo.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'K0REWAN@ND3SUKA?!?!'   


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

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

@app.route('/login.html', methods = ['GET','POST'])
def login():
    users = User.query.all()
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if user:
            if(check_password_hash(user.password, password)):
                login_user(user)
                return redirect(url_for('home', user=user, lists=lists))
            else:
                flash("This is sad")
        else:
            flash('This username does not exist')
    
    return render_template('login.html')

@app.route('/signup.html', methods = ['GET','POST'])
def signup():
    users = User.query.all()
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        for user in users:
            if user.username == username:
                flash('This username is already taken, please try again.')
                return redirect(url_for('signup'))

        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('home', user=user, lists=lists))
        
    return render_template('signup.html')

@app.route('/lists.html')
def lists():
    if current_user.is_authenticated:
        lists = List.query.filter_by(user_id= current_user.id ).all()
        return render_template('lists.html', lists=lists)
    else: 
        return "Error: user is not logged in"
        

@app.route('/lists/<int:list_id>/', methods = ['GET', 'POST'])
def showlist(list_id):
    if current_user.is_authenticated:  
        list = List.query.get_or_404(list_id)

        if list.id != current_user.id:
            return "Error: You do not have access"
        else:
            lists = List.query.filter_by(user_id=current_user.id).all()
            listItems = ListItem.query.filter_by(list_id=list_id).all()
            completed = ListItem.query.filter_by(list_id=list_id, completed=True).all()
            uncompleted = ListItem.query.filter_by(list_id=list_id, completed=False).all()
            return render_template('list.html', list=list, lists=lists, completed=completed, uncompleted=uncompleted)
    else:
        return "Error: user is not logged in"
    
    return render_template('list.html', list=list, lists=lists, completed=completed, uncompleted=uncompleted)

      
    
@app.route('/newlist.html', methods = ['GET','POST'])
def newlist():

    if current_user.is_authenticated:
        lists = List.query.filter_by(user_id=current_user.id).all()
        userid = current_user.id
    else: 
        return "Error: user is not logged in"

    if request.method == "POST":
        listname = request.form["listname"]
        count = request.form["countTracker"]

        qrytext = text("INSERT INTO LISTS (name, user_id) VALUES (:listname, :userid);") 
        qry = qrytext.bindparams(listname=listname, userid=userid)
        db.session.execute(qry) 
        db.session.commit() 

        list = List.query.filter_by(name=listname).first()
        listid = list.id

        for i in range(1, int(count)):
            itemname = request.form["listitem" + str(i)]
            qrytext = text("INSERT INTO ITEMS (name, completed, list_id) VALUES (:itemname, False, :listid);") 
            qry = qrytext.bindparams(itemname=itemname, listid=listid)
            db.session.execute(qry) 
            
        db.session.commit()

        return redirect(url_for('lists', lists=lists))

    return render_template('newlist.html', lists=lists)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/navbar.html')
def navbar():
    if current_user.is_authenticated:
        lists = List.query.filter_by(user_id=current_user.id ).all()
        return render_template('navbar.html', lists=lists)
    else: 
        return "Error: user is not logged in"

@app.route('/home.html')
def home():
    if current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.id ).first()
        lists = List.query.filter_by(user_id=current_user.id ).limit(5).all()
        return render_template('home.html', user=user, lists=lists)
    else: 
        return "Error: user is not logged in"

@app.route('/list' , methods = ['GET', 'POST'])
def post():
    if request.is_json:
        if request.method == "POST":
            activity = json.loads(request.data).get("activity")

            if activity == "check":
                returnid = json.loads(request.data).get("id")
                listItem = ListItem.query.filter_by(id = returnid).first()
                completed = listItem.completed
                listItem.completed = not completed
                db.session.commit()
            if activity == "add":
                content = json.loads(request.data).get("content")
                listid = json.loads(request.data).get("id")
                listItem = ListItem(content, False, listid)
                db.session.add(listItem)
                db.session.commit()

            return jsonify({'valid': "Yes"})

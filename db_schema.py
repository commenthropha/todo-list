from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
db.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///db_schema.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Users(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(10))
    password = db.Column(db.String(25))
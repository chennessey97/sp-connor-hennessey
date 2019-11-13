from flask_login import UserMixin
from . import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)  # primary keys are required by SQLAlchemy
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100))
    image = db.Column(db.String(50), nullable=False, default='static/user.png')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Transaction(db.Model):
    __tablename__ = 'transactions'
    transID = db.Column(primary_key=True)
    date = db.Column()
    description = db.Column()
    category = db.Column()
    amount = db.Column()
    userID = db.Column()

class FileInput(db.Model):
    __tablename__ = 'input'
    id = db.Column(db.Integer(), unique=True, nullable=False)
    user = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100))  # file name?
    date = db.Column(db.DateTime())

class Goal(db.Model):
    __tablename__ = 'goals'
    id = db.Column(db.Integer(), unique=True, nullable=False)
    userID = db.Column(db.Integer(), nullable=False)
    goal = db.Column(db.Integer(), nullable=False)
    # totalspent = db.Column(db.Integer())
    # shouldsave = db.Column(db.Integer())


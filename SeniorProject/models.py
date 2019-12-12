from flask_login import UserMixin
from . import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)  # primary keys are required by SQLAlchemy
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100))
    image = db.Column(db.String(50), nullable=False, default='static/icons/user.png')
    goal = db.Column(db.Integer(), nullable=True, default='null')
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
    uploadID = db.Column()


class FileInput(db.Model):
    __tablename__ = 'input'
    id = db.Column(db.Integer(), unique=True, nullable=False)
    userID = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100))  # file name?
    date = db.Column(db.DateTime())


class Chart(db.Model):
    __tablename__ = 'charts'
    chartID = db.Column(db.Integer(), primary_key=True, unique=True, nullable=False)
    type = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime())
    path = db.Column(db.String(100))
    userID = db.Column(db.String(100), nullable=False)


class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer(), primary_key=True, unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False, default='New Note ')
    author = db.Column(db.String(), nullable=False, default=User.username)
    date = db.Column(db.DateTime(), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    userID = db.Column(db.Integer(), nullable=False)
    img = db.Column(db.String(100), default=User.image)


class Nums(db.Model):
    __tablename__ = 'nums'
    userID = db.Column(db.Integer(), primary_key=True, unique=True, nullable=False)
    last_total = db.Column()
    current_total = db.Column()
    all_total = db.Column()
    active_goal = db.Column()
    #current_cats = db.Column()
    #last_cats = db.Column()



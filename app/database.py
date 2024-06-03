from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    pwhash = db.Column(db.String(128), nullable=False)

    icon = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def __init__(self, name, email, password, icon=1, score=0):
        self.name = name
        self.email = email
        self.pwhash = bcrypt.generate_password_hash(password, 12).decode('utf-8')
        self.icon = icon
        self.score = score

    def check_password(self, password):
        return bcrypt.check_password_hash(self.pwhash, password)

    def __repr__(self):
        return '<User %r>' % self.name


class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(15), nullable=False)
    lastname = db.Column(db.String(15), nullable=False)
    subject = db.Column(db.String(500), nullable=False)

    def __init__(self, firstname, lastname, subject):
        self.firstname = firstname
        self.lastname = lastname
        self.subject = subject

    def __repr__(self):
        return '<User %r>' % self.firstname + self.lastname

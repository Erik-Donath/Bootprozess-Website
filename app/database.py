from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    pwhash = db.Column(db.String(128), nullable=False)

    score = db.Column(db.Integer, nullable=False)

    def __init__(self, username, email, password, score=0):
        self.username = username
        self.email = email
        self.pwhash = bcrypt.generate_password_hash(password, 12).decode('utf-8')
        self.score = score

    def check_password(self, password):
        return bcrypt.check_password_hash(self.pwhash, password)

    def __repr__(self):
        return '<User %r>' % self.username


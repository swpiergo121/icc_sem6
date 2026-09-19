#!/usr/bin/env python3


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@flask_db:5432/postgres"
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, username, password, email, role):
        self.username = username
        self.password = password
        self.email = email
        self.role = role

    def json(self):
        return {'id': self.id,'username': self.username, 'email': self.email, "role": self.role}


def start_database():
    new_user = User(username="Jhon smit", password="1234", email="js@gmail.com", role="usuario")
    db.session.add(new_user)

    new_user = User(username="James Bond", password="qwerty", email="j007@mi6.uk", role="admin")
    db.session.add(new_user)

    db.session.commit()

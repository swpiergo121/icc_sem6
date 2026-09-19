#!/usr/bin/env python3

from os import environ
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, url_for, redirect, make_response, jsonify


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {'id': self.id,'username': self.username, 'email': self.email}


db.create_all()

@app.route('/select')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/create/', methods=('GET','POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        new_user = User(username=name, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/users/<int:id>', methods=['PUT', 'GET'])
def update_user(id):
    if request.method == "Put":
        user = User.query.filter_by(id=id).first()
        if user:
            name = request.form['name']
            password = request.form['password']
            email = request.form['email']
            if name != "":
                user.username = name
            if password != "":
                user.password = password
            if email != "":
                user.email = email
            db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html')

# delete a user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      db.session.delete(user)
      db.session.commit()
      return redirect(url_for('index'))
    return make_response(jsonify({'message': 'user not found'}), 404)
  except e:
    return make_response(jsonify({'message': 'error deleting user'}), 500)

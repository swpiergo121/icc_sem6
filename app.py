#!/usr/bin/env python3

from os import environ
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, url_for, redirect, make_response, jsonify
from database import db, User, app


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
        role = request.form['role']
        new_user = User(username=name, password=password, email=email, role=role)
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
            role = request.form['role']
            if name != "":
                user.username = name
            if password != "":
                user.password = password
            if email != "":
                user.email = email
            if role != "":
                user.role = role
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


@app.route('/', methods=['GET, "POST"'])
def login():
    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']
        if name != "" and password != "":
            user = User.query.filter_by(name=name).first()
            if user != None and user.password == password:
                return redirect(url_for('index'))
        return render_template('login.html')
    else:
        return render_template('login.html')


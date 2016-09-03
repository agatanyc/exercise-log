"""Main module of an aplication for loging exercises."""

from flask import Flask, render_template, request, make_response
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

from app import app
from model import User, Exercise, UserExercise, HTTPSession, init_db, db

init_db(app)

"""
@app.route('/user/<username>')
def show_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('show_user.html', user=user)
"""
@app.route('/')
def index():
    if logged_in():
        return render_template(log_workout.html) #TODO
    else:
        return render_template('login.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST' and logged_in():
        redir = redirect('/entry')
        resp = app.make_response(redir)
        UUID = uuid4()
        resp.set_cookie('session_id', "UUID")
        
        user_name = request.form['username']
        password = request.form['passsword']
        user = db.session.query(User).filter(username=user_name,
                password=password)
        if user and password:
            user_id = logged_in()
            new_row = HTTPSession(session_cookie=UUID, user_id=user_id)
            db.session.add(new_row)
            db.session.commit()
            return resp
    else:
        return index()

@app.route('/logout')
def logout():
    # remove the user_id and cookie from the session
    HTTPSession.query.filter(HTTPSession.session_cookie==UUID).delete()
# pull the uuid from the cookie and delete that!#TODO
    return redirect(url_for('/'))

@app.route('/entry')
def entry():
    return render_template('log_workout.html')

# Helper functions

def logged_in():
    if request.cookies.get('session_id'):
        for sess in db.session.query(HTTPSession).filter(
                HTTPSession.session == request.cookie.get('session_id')):
            return sess.user_id
    return None

def cookie():
    cookie = request.cookies.get('session_id')

if __name__ == "__main__":
    app.debug = True

    init_db(app)
    app.run()

# select user_id from sessions where session = "jj";DROP DATABASE;ttt"
# create class Session
# create sessions table
# query the db for the record where cookie uuid == session uuid
#
# session.query(Session).filter(Session.session == request.cookie.get('session_id'))
# return user_id coresponding with the session uuid in sessions table
# meaning user loged in or None
# SET COOKIE in login function and every time user changes endpoint.

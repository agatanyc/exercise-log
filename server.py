"""Main module of an aplication for loging exercises."""

from flask import Flask, render_template, request, make_response, redirect, \
                  url_for
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
        return render_template('log_workout.html') #TODO
    else:
        return render_template('login.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        render =  render_template('log_workout.html')
        resp = make_response(render)
        UUID = uuid4()
        resp.set_cookie('session_id', str(UUID))
        
        user_name = request.form['username']
        password = request.form['password']
        users = db.session.query(User).filter(User.user_name==user_name,
                User.password==password)
        for user in users:
            user_id = user.user_id
            new_row = HTTPSession(session_cookie=str(UUID), user_id=user_id)
            db.session.add(new_row)
            db.session.commit()
            return resp
        return "Invalid username and/or password"
    else:
        return index()

@app.route('/logout')
def logout():
    # remove the user_id and cookie from the session
    db.session.query(HTTPSession).filter(HTTPSession.session_cookie ==
                             request.cookies.get('session_id')).delete()
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/entry', methods=['GET','POST'])
def entry():
    if request.method == 'POST':
        exercise_name = request.form['exercise']
        weight = request.form['weight']
        reps = request.form['reps']
        time = request.form['time']
        date = request.form['date']

        current_line = UserExercise(exercise_id=exercise_id, user_id=user_id,
                                 weight=weight, reps=reps, time=time,
                                 date=date)
        db.session.add(current_line)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('log_workout.html')
        
    # 'form' format, get the data and save it in the DB
    # FOrm is the way for a browser to construct the data the user provides
    # if the the method is GET - return webpage with a 'form' 
    # to enter a workout data
    # if POST process the data from the 'form', save to the DB and give feedback
    # to the user.
    return render_template('log_workout.html')

@app.route('/history', methods=['GET','POST'])
def workout_history():
    if request.method == 'GET':
        current_user = logged_in()
        if current_user:
            history = db.session.query(UserExercise).filter(UserExercise.user_id ==
                                                         current_user).all() 
            db.session.commit()
            return render_template('history.html')
        else:
            return render_template('login.html')
    else:
        # there is a POST request

        # there is a request to edit the history data
        # loop through all entry columns, check which was edited and commit it 
        # to the db
        # use template to display data dinamicly - use templating
        # provide a link to edit the workout if needed

        # pull data from UserExercise table and display it e.g. name of exercise 
        # not the exercise id
        pass

# Helper functions

def logged_in():
    if request.cookies.get('session_id'):
        for sess in db.session.query(HTTPSession).filter(
                HTTPSession.session_cookie == request.cookies.get('session_id')):
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
#
#Get the cookie from the req and set it  in every view function. Pbly in logged_in function.

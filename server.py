"""Main module of an aplication for loging exercises."""

from flask import Flask, render_template, request, make_response, redirect, \
                  url_for
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from datetime import date

from app import app
from model import User, Exercise, UserExercise, HTTPSession, init_db, db

init_db(app)

@app.route('/')
def index():
    if logged_in():
        return redirect(url_for('entry'))
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        resp = redirect(url_for('entry'))
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
        return render_template('login.html')

@app.route('/logout')
def logout():
    # remove the user_id and cookie from the session
    db.session.query(HTTPSession).filter(HTTPSession.session_cookie ==
                             request.cookies.get('session_id')).delete()
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/entry', methods=['GET','POST'])
def entry():
    # if the the method is GET - return webpage with a 'form' 
    # to enter a workout data
    # if POST process the data from the 'form', save to the DB and give
    # feedback to the user
    # return render_template('entry.html')
    if request.method == 'POST':
        user_id = logged_in()
        exercise_id = request.form['exercise_id']
        weight = request.form['weight']
        reps = request.form['reps']
        time = request.form['time']
        year, month, day = request.form['date'].split('-') #e.g.['2016', '09', '11']
        d = date(int(year), int(month), int(day)) 
        new_row = UserExercise(exercise_id=exercise_id, user_id=user_id,
                                 weight=weight, reps=reps, time=time,
                                 date=d)
        db.session.add(new_row)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        if logged_in():
            rows = db.session.query(Exercise).all()
            exercises = {}
            for row in rows: #TODO move it to a function
                exercise_name = row.exercise
                exercise_id = row.exercise_id
                exercises[exercise_id] = exercise_name
            return render_template('entry.html', exercises=exercises)
        else:
            return redirect(url_for('login'))

@app.route('/edit', methods=['GET','POST'])
def edit_history():
    if request.method == 'GET':
        if logged_in():
            query_string = request.args.to_dict()
            user_exercise_id = query_string['id']
            # rows is a list of UserExercise instances
            # (in this case it will be list of one instance)
            user_exercise_rows = db.session.query(UserExercise).filter(
                      UserExercise.user_exercise_id == user_exercise_id).all() 
            for workout in user_exercise_rows:
                pass

            exercise_rows = db.session.query(Exercise).all()
            exercises = {}
            for row in exercise_rows:
                    exercise_name = row.exercise
                    exercise_id = row.exercise_id
                    # exercises is a dict passed to the html file 
                    exercises[exercise_id] = exercise_name
                    #TODO move it to a function
            return render_template('edit.html', workout=workout,
                                          exercises=exercises)
    else:
        user_exercise = db.session.query(UserExercise).filter(
                UserExercise.user_exercise_id == request.form['user_exercise_id']).all() 
        for u_e in user_exercise:
            u_e.user_id = logged_in()
            u_e.exercise_id = request.form['exercise_id']
            u_e.weight = request.form['weight']
            u_e.reps = request.form['reps']
            u_e.time = request.form['time']
            year, month, day = request.form['date'].split('-') #e.g.['2016', '09', '11']
            u_e.d = date(int(year), int(month), int(day)) 

        db.session.commit()
    return redirect(url_for('index'))
        
@app.route('/history', methods=['GET','POST'])
def workout_history():
    if request.method == 'GET':
        current_user = logged_in()
        if current_user:
            rows = db.session.query(UserExercise).filter(
                                  UserExercise.user_id == current_user).all() 

            return render_template('history.html', workouts=rows)
        else:
            return render_template('login.html')

# Helper functions

def logged_in():
    if request.cookies.get('session_id'):
        for sess in db.session.query(HTTPSession).filter(
                HTTPSession.session_cookie == request.cookies.get('session_id')):
            return sess.user_id
    return None

def cookie():
    cookie = request.cookies.get('session_id')
    return cookie

if __name__ == "__main__":
    app.debug = True

    init_db(app)
    app.run()


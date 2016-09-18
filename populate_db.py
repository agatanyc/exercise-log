"""File to populate the db."""

from model import init_db, db, User, Exercise, UserExercise, HTTPSession
from app import app
import sqlite3
from datetime import datetime

def load_user():
    user_name = 'admin'
    password = 'password'
    current_line = User(user_name=user_name, password=password)
    db.session.add(current_line)
    db.session.commit()

def load_exercise():
    exercise_names = ['Squat', 'DL', 'Bench press', 'Seated Row', 'Pushup']
    for e in exercise_names:
        current_line = Exercise(exercise=e)
        db.session.add(current_line)
        db.session.commit()

def load_user_exercise():
    exercise_id = 1
    user_id = 1
    weight = 135
    reps = 10
    time = ''
    date = datetime.utcnow()

    current_line = UserExercise(exercise_id=exercise_id, user_id=user_id,
                                 weight=weight, reps=reps, time=time,
                                 date=date)
    db.session.add(current_line)
    db.session.commit()

def load_session():
    session_id = 1
    session_cookie = '14958e74-ce37-4b3b-80a8-e0687e4b6d70'
    user_id = 1
    current_line = HTTPSession(session_id=session_id,
                           session_cookie=session_cookie, user_id=user_id)
    db.session.add(current_line)
    db.session.commit()


if __name__ == "__main__":

    init_db(app)
    db.create_all()

    load_user()
    load_exercise()
    load_user_exercise()
    load_session()

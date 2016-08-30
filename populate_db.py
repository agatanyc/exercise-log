"""File to populate the db."""
from model import connect_to_db, db, User, Exercise, UserExercise
from server import app
import sqlite3

def load_user():
    user_name = 'Agata'
    password = '123'
    current_line = User(user_name=user_name, password=password)
    db.session.add(current_line)
    db.session.commit()

def load_exercise():
    exercise = 'squat'
    current_line = Exercise(exercise=exercise)
    db.session.add(current_line)
    db.session.commit()

def load_user_exercise():
    exercise_id = 1
    user_id = 1
    weight = 135
    reps = 10
    time = ''
    current_line = UserExercise(exercise_id=exercise_id, user_id=user_id,
            weight=weight, reps=reps, time=time)
    db.session.add(current_line)
    db.session.commit()

if __name__ == "__main__":

    connect_to_db(app)
    db.create_all()

    load_user()
    load_exercise()
    load_user_exercise()

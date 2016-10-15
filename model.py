from flask_sqlalchemy import SQLAlchemy
from app import app
from datetime import datetime

db = SQLAlchemy(app)

# Model definitions

class User(db.Model):

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_name = db.Column(db.String(40))
    password = db.Column(db.String(30))
    user_exercises = db.relationship('UserExercise',back_populates='user')
    sessions = db.relationship('HTTPSession', back_populates='user')

    def __repr__(self):
        return "<User user_id:%s name=%s" % (self.user_id, self.user_name)

class Exercise(db.Model):
    
    __tablename__ = "exercises"

    exercise_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    exercise = db.Column(db.String(50), nullable=False)
    user_exercises = db.relationship('UserExercise', back_populates='exercise')

    def __repr__(self):
        return "<Exercise exercise_id=%s name=%s" % (self.exercise_id,
                                                     self.exercise)   

class UserExercise(db.Model):

    __tablename__ = "user_exercises"

    user_exercise_id = db.Column(db.Integer, autoincrement=True,
                                 primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                                                  nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.exercise_id'),
                   nullable=False)
    weight = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    time = db.Column(db.String(30))
    date = db.Column(db.DateTime)

    user = db.relationship('User', back_populates='user_exercises')
    exercise = db.relationship('Exercise', back_populates='user_exercises')


class HTTPSession(db.Model):

    __tablename__ = "sessions"

    session_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    session_cookie = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                                                  nullable=False)
    user = db.relationship('User', back_populates='sessions')

#--------------------------

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workouts.db'
    db.app = app
    db.init_app(app)

if __name__ == "__main__":

    init_db(app)
    print "Connected to DB"

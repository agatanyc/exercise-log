from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Model definitions

class User(db.Model):

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_name = db.Column(db.String(40))
    username = db.Column(db.String(20))
    password = db.Column(db.String(30))

    def __repr__(self):
        return "<User user_id:%s name=%s" % (self.user_id, self.user_name)

class Exercise(db.Model):
    
    __tablename__ = "exercises"

    exercise_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    exercise = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "<Exercise exercise_id=%s name=%s" % (self.exercise_id, self.exercise)   

class UserExercise(db.Model):

    __tablename__ = "user_exercises"

    user_exercise_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.exercise_id'),
                   nullable=False)
    weight = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    time = db.Column(db.String(30))

    # Define relationship to 'User' and `Exercise` class
    exercise = db.relationship("Exercise", backref=db.backref("user_exercises"))
    user = db.relationship("User", backref=db.backref("user_exercises"))

#--------------------------

# Helper functions

def connect_to_db(app):

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workouts.db'
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    from server import app

    connect_to_db(app)
    print "Connected to DB"

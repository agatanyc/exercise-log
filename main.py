"""Main module of an aplication for loging exercises."""


from flask import Flask, Response, render_template, redirect, request
from flask_login import UserMixin, LoginManager, \
    login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)

# user class for providing authentication
# UserMixin methods are described at:
# https://flask-login.readthedocs.io/en/latest/


class User(UserMixin):     #TODO add db.Model base class afetr db is setup

    def __init__(self, user_id):
        self.id = user_id

@app.route('/', methods=['GET'])
def index():
    return 'HELLO!'

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usermail = request.form['usermail']
        password = request.form['password']
        if check_auth(usermail, password):
            return render_template('welcome.html')
        else:
            return render_template('login.html', error='Invalid user name and password.')
    else:
         return render_template('login.html')
        
def check_auth(usermail, password):
    """Validate user's credentials."""
    return usermail == 'agata78@gmail.com' and password  == '123'


if __name__ == '__main__':
    app.run(debug=True) #port=8000, use_reloader=True

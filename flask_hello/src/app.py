from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired 

import mydb
import sqlite3

app = Flask(__name__)

CSRF_ENABLED = True
app.config['SECRET_KEY'] = "sdxLWlkwejWLEKwvbsmdXXMCVBWEUwefoimHf"

conn = sqlite3.connect("test.db")
conn.cursor().execute("create table if not exists users (username text, password text, email text)")
conn.commit

print(conn.cursor().execute("select * from users").fetchall())

class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


class MyForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])

class MyFormWithEmail(MyForm):
    email = StringField('email', validators=[DataRequired()])

@app.route('/')
def index():
    return render_template('index.html', form=MyForm())

@app.route('/login', methods=['POST'])
def submit_login():
    form = MyForm()
    if form.validate_on_submit():
        if mydb.areValidCredentials(form.username.data, form.password.data):
            return "success login"
        else:    
            return "such user does not exist"
    else:
        print("form invalid")
        print(form.errors)
        return render_template('index.html', form=form)

@app.route('/signup', methods=['POST'])
def submit_signup():
    form = MyFormWithEmail()
    if form.validate_on_submit():
        if mydb.containsUser(form.username.data):
            return "user already exist"
        else:   
            mydb.createUser(form.username.data, form.password.data, form.email.data)
            return "success signup"
    else:
        print("form invalid")
        print(form.errors)
        return render_template('index.html', form=form)
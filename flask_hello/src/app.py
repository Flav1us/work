from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

from db.user_db import UserDb
import sqlite3

app = Flask(__name__)

CSRF_ENABLED = True
app.config['SECRET_KEY'] = "sdxLWlkwejWLEKwvbsmdXXMCVBWEUwefoimHf"

conn = sqlite3.connect("test.db")
conn.cursor().execute("create table if not exists users (username text, password text, email text)")
conn.commit

print(conn.cursor().execute("select * from users").fetchall())

mydb = UserDb()


class MyForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])

    @property
    def name(self):
        return self.username.data


class MyFormWithEmail(MyForm):
    email = StringField('email', validators=[DataRequired()])
    accept = BooleanField('accept')


@app.route('/')
def index():
    return render_template('index.html', form=MyForm())


@app.route('/login', methods=['POST'])
def submit_login():
    form = MyForm()
    if form.validate_on_submit():
        if mydb.are_valid_credentials(form.username.data, form.password.data):
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
        if mydb.contains_user(form.username.data):
            return "user already exist"
        else:
            mydb.create_user(form.name, form.password.data, form.email.data)
            return "success signup"
    else:
        print("form invalid")
        print(form.errors)
        return render_template('index.html', form=form)

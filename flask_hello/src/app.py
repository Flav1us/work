from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from flask_user import UserManager, login_required
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

from db.user_db import UserDb
from db.models import User
from logger import log


# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = 'sdxLWlkwejWLEKwvbsmdXXMCVBWEUwefoimHf'

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'    # File-based SQL database
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning

    # Flask-User settings
    USER_APP_NAME = "Flask-User test"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = False      # Disable email authentication
    USER_ENABLE_USERNAME = True    # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = False    # Simplify register form


app = Flask(__name__)
app.config.from_object(__name__+'.ConfigClass')

CSRF_ENABLED = True
# app.config['SECRET_KEY'] = "sdxLWlkwejWLEKwvbsmdXXMCVBWEUwefoimHf"

sqla_db = SQLAlchemy(app)
mydb = UserDb()

user_manager = UserManager(app, sqla_db, User)


class MyForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])

    @property
    def name(self):
        return self.username.data

    @property
    def passwd(self):
        return self.password.data


class MyFormWithEmail(MyForm):
    email = StringField('email', validators=[DataRequired()])
    accept = BooleanField('accept')

    @property
    def e_mail(self):
        return self.email.data

    @property
    def is_accepted(self):
        return self.accept.data


@app.route('/')
def index():
    return render_template('index.html', form=MyForm())


@app.route('/login', methods=['POST'])
def submit_login():
    form = MyForm()
    if form.validate_on_submit():
        log(log.INFO, 'Login user %s', form.name)
        if mydb.are_valid_credentials(form.name, form.passwd):
            log(log.INFO, 'login successed')
            return "success login"
        else:
            log(log.WARNING, 'login failed')
            return "such user does not exist"
    else:
        log(log.ERROR, 'form invalid')
        log(log.ERROR, form.errors)
        return render_template('index.html', form=form)


@app.route('/signup', methods=['POST'])
def submit_signup():
    form = MyFormWithEmail()
    log(log.INFO, 'New user: %s', form.name)
    if form.validate_on_submit():
        if mydb.contains_user(form.name):
            log(log.WARNING, 'user alredy exists')
            return "user already exists"
        else:
            mydb.create_user(form.name, form.passwd, form.e_mail)
            log(log.INFO, 'user succesfully added')
            return "success signup"
    else:
        log(log.ERROR, 'form invalid')
        log(log.ERROR, form.errors)
        return render_template('index.html', form=form)


@app.route('/cabinet')
@login_required
def get_cabinet():
    return render_template('cabinet.html', username='user')

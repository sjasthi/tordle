import requests
import json
import random
from datetime import datetime, date, timedelta
from flask import (
    Flask,
    render_template,
    url_for,
    redirect,
    request,
    flash,
    abort,
    session,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

# from flask_login.login_manager import LoginManager
from flask_login import (
    login_user,
    current_user,
    logout_user,
    login_required,
    UserMixin,
    LoginManager,
)
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    TextAreaField,
    SelectField,
)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

# from flask_bcrypt import Bcrypt

from telugu import getTeluguLogicalChars, isTeluguWord, isEnglish

app = Flask(__name__)
app.config["SECRET_KEY"] = "5791628bb0b13ce0c676dfde280ba245"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/tordle.db"
app.config["USER_APP_NAME"] = "Tordle Game App"
app.config["USER_ENABLE_EMAIL"] = False  # Disable email authentication
app.config["CSRF_ENABLE"] = True
# app.config["SECURITY_PASSWORD_HASH"] = "bcrypt"
# app.config["SECURITY_PASSWORD_SALT"] = "$2a$16$PnnIgfMwkOjGX4SkHqSOPO"
db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
# session.permanent = True
app.permanent_session_lifetime = timedelta(days=1)


# @app.before_first_request
# def make_session_permanent():
#     session["ping"] = "pong"
#     print("befor first request seesion: " + session["ping"])

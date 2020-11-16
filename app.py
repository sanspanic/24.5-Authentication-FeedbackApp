from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from secrets import secret
#from forms import UserForm, TweetForm
#from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///feedback_app"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = secret
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True


connect_db(app)

toolbar = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    return 
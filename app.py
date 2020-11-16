from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from secrets import secret
from forms import RegisterForm, LoginForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///feedback_app"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = secret
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)

toolbar = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register(): 

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)

        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken. Please pick another.')
            return render_template('register.html', form=form)

        session['user_id'] = new_user.id
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect('/secret')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login(): 

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            flash(f"Welcome Back, {user.username}!", "info")
            session['user_id'] = user.id
            return redirect('/secret')
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)

@app.route('/secret')
def show_user_info(): 
    if 'user_id' not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    
    return render_template('user_info.html')

@app.route('/logout')
def logout_user():
    session.pop('user_id')
    flash("Goodbye!", "info")
    return redirect('/')

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from uuid import uuid1
from .models import User
from .forms import RegistrationForm, LoginForm
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html', form=LoginForm())

@auth.route("/login", methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()
    # check if user exists - take the user supplied password, hash it, and compare it to the hashed password in db
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.', 'alert-error')
        return redirect(url_for('auth.login'))  # if user doesn't exist or password is wrong, reload the page
    login_user(user, remember=remember)  # if the above check passes, then we know the user has the right credentials
    return redirect(url_for('main.profile'))


@auth.route('/register')
def register():
    return render_template('register.html', form=RegistrationForm())

@auth.route("/register", methods=['POST'])
def register_post():
    e = request.form.get('email')
    u = request.form.get('username')
    p = request.form.get('password')
    i = uuid1().time_low
    user = User.query.filter_by(email=e).first()  # if this returns a user, then the email already exists in db
    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists', 'alert-error')
        return redirect(url_for('main.register'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(username=u, email=e, password=generate_password_hash(p, method='sha256'), id=i)
    db.session.add(new_user)  # add the new user to the database
    db.session.commit()
    flash('Welcome to Dough!', category='alert-success')
    return redirect(url_for('auth.login'))  # auth.login


@auth.route('/logout')  # ***** add message?
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from .forms import RegistrationForm, LoginForm
from . import db

main = Blueprint('main', __name__)


@main.route('/')  # Root/Home page
@main.route("/home", methods=['GET', 'POST'])  # Root/Home page
def home():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created for {form.username.data}!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('home.html', title='Home', form=form)


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@main.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard')


@main.route("/data")
@login_required
def data():
    return render_template('data.html', title='User Data')


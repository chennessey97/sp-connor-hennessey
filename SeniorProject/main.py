import secrets
from PIL import Image
from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request, flash, app
from uuid import uuid1
from flask_login import login_user, logout_user, login_required
from .models import User, Spreadsheet, FileInput, Transaction
from .forms import RegistrationForm, LoginForm, UpdateAccountForm
from . import db
import os
from werkzeug.security import generate_password_hash, check_password_hash
import urllib.request
from werkzeug.utils import secure_filename
import pandas as pd
from pandas import ExcelWriter, ExcelFile
import sqlite3
from datetime import datetime


main = Blueprint('main', __name__)


@main.route('/')  # Root/Home page
@main.route("/home", methods=['GET', 'POST'])  # Root/Home page
def home():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created for {form.username.data}!', 'alert-success')
        return redirect(url_for('dashboard'))
    return render_template('home.html', title='Home', form=form)


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route('/profile')
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            # picture_file = request.files['file']
            current_user.image = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', category='alert-success')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET' or 'POST':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='static/profile_pics/' + current_user.image)
    return render_template('profile.html', title='Profile', image=image_file, form=form)


@main.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard')


@main.route("/data")
@login_required
def data():
    return render_template('data.html', title='User Data', action=data_upload())

def allowed_file(filename):  # necessary? ************************************************************
    ALLOWED_FILES = {'.xlsx', '.xls'}
    return redirect('main.data') in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_FILES

@main.route("/data", methods=['POST'])
@login_required
def data_upload():
    if request.method == 'POST':
        # check if the post request has the file part
        #if 'example.xlsx' not in request.files:
        #    flash('No file!', category='alert-error')
        #    return render_template('data.html') #****************************************************
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading', category='alert-error')
            return render_template('data.html')
        if file:  # and allowed_file(file.filename): **************************************************
            filename = file.filename
            date = datetime.now()
            new_input = FileInput(id=uuid1().time_low, user=current_user.username, name=filename, date=date)
            #check = FileInput.query.filter_by(name=filename).first()  # if this returns a user, then the email already exists in db
            #if check:  # if a user is found, we want to redirect back to signup page so user can try again
            #    flash('File already exists', 'alert-error')
            #    return redirect(url_for('main.data'))
            db.session.add(new_input)
            db.session.commit()

            cols = [1, 2, 4, 6]
            df = pd.read_excel('SeniorProject/uploads/example.xlsx', usecols=cols)
            df.update('"' + df[['Date', 'Original Description', 'Category', 'Amount']].astype(str) + '"')
            for i, row in df.iterrows():
                r = Transaction(transID=uuid1().time_low, date=row['Date'], description=row['Original Description'], category=row['Category'], amount=row['Amount'], userID=current_user.id)
                db.session.add(r)
                db.session.commit()
            file.save(secure_filename(file.filename))
            flash("File Successfully Uploaded!", category='alert-success')
            return render_template('data.html')
        else:
            flash('Allowed file type is .xlsx')
            return render_template('data.html')


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join('C:/Users/Connor/PycharmProjects/sp-connor-hennessey', 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn



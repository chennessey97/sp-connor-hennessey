import os
from . import db
from .models import User, FileInput, Transaction, Chart, Note
from .forms import RegistrationForm, LoginForm, UpdateAccountForm, DataTable, NoteForm, Filter
from PIL import Image
from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request, flash, app
from uuid import uuid1
from flask_login import login_user, logout_user, login_required
import pandas as pd
import plotly
import plotly.graph_objects as go
from plotly import tools as tls
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import plotly.io as pio
import plotly.express as px
from matplotlib.artist import setp
from jinja2 import Template
# import imgkit   from werkzeug.security import generate_password_hash, check_password_hash   import urllib.request   from werkzeug.utils import secure_filename   from pandas import ExcelWriter, ExcelFile   import secrets

main = Blueprint('main', __name__)

# conn = sqlite3.connect('C:/Users/Connor/PycharmProjects/sp-connor-hennessey/SeniorProject/db.sqlite')
database = 'C:/Users/Connor/PycharmProjects/sp-connor-hennessey/SeniorProject/db.sqlite'

def create_connection(database):
    conn = None
    try:
        conn = sqlite3.connect(database, check_same_thread=False)
    except sqlite3.Error as e:
        print(e)
    return conn

conn = create_connection(database)
# cursor = conn.cursor()

@main.route('/')  # Root/Home page
@main.route("/home", methods=['GET', 'POST'])  # Root/Home page
def home():
    notes = Note.query.all()
    form = Filter()
    if form.validate_on_submit():
        f = form.filter.data
        if f == 'all_posts':
            notes = Note.query.all()
            flash('All Posts', 'alert-neutral')
            return render_template('home.html', title='Home', form=form, notes=notes)
        if f == 'my_posts':
            notes = [x for x in notes if x.author == current_user.username]
            flash('My Posts', 'alert-neutral')
            return render_template('home.html', title='Home', form=form, notes=notes)
        if f == 'suggestions':
            notes = [x for x in notes if 'Dough Suggestion' in x.author]
            flash('My Suggestions', 'alert-neutral')
            return render_template('home.html', title='Home', form=form, notes=notes)
        if f == 'other_posts':
            notes = [x for x in notes if x.author != current_user.username]
            flash('Other Posts', 'alert-neutral')
            return render_template('home.html', title='Home', form=form, notes=notes)

    return render_template('home.html', title='Home', notes=notes, form=form)


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image = "static/profile_pics/"+picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', category='alert-success')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET' or 'POST':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image)
    return render_template('profile.html', title='Profile', image=image_file, form=form)


def save_picture(form_picture):  # returns name of picture file
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = form_picture.filename+"_"+str(current_user.id)+f_ext
    picture_path = os.path.join('C:/Users/Connor/PycharmProjects/sp-connor-hennessey/SeniorProject', 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@main.route("/data")
@login_required
def data():
    return render_template('data.html', title='User Data', action=data_upload())

def allowed_file(filename):
    ALLOWED_FILES = {'.xlsx', '.xls'}
    return redirect('main.data') in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_FILES

@main.route("/data", methods=['POST'])
@login_required
def data_upload():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading', category='alert-error')
            return render_template('data.html')
        if file:
            filename = file.filename
            file.save('SeniorProject/static/uploads/'+filename)

            date = datetime.now()
            new_input = FileInput(id=uuid1().time_low, userID=current_user.id, name=filename, date=date)
            db.session.add(new_input)
            db.session.commit()

            cols = [1, 2, 4, 6]
            df = pd.read_excel('SeniorProject/static/uploads/'+filename, usecols=cols)
            df.update('"' + df[['Date']].astype(str) + '"')
            for i, row in df.iterrows():
                r = Transaction(transID=uuid1().time_low, date=row['Date'], description=row['Original Description'], category=row['Category'], amount=row['Amount'], userID=current_user.id)
                db.session.add(r)
                db.session.commit()
            flash("File Successfully Uploaded!", category='alert-success')
            return render_template('data.html')
        else:
            flash('Allowed file type is .xlsx')
            return render_template('data.html')


@main.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    form = DataTable()
    userid = current_user.id
    html = generate_chart_table(userid)
    if form.set_goal.data:
        set_new_goal(form.set_goal.data)
    if form.validate_on_submit():
        #if not has_data(userid, conn):
        #    flash('You have not uploaded any data yet. Input an excel spreadsheet with your finances.', category='alert-error')
        #    return render_template('dashboard.html', title='Dashboard', form=form)
        #else:
        option = form.data_views.data
        print(option)
        if option == 'data_view':

            x = generate_chart_raw(userid)
        if option == 'type_view':
            x = generate_chart_pie(userid)
        if option == 'all_spending_view':
            x = generate_chart_bar(userid)
        if option == 'progress_view':
            x = generate_chart_progress(userid)

        if form.make_note.data:  # ********************************************************************************
            quick_note(form.make_note.data)
        if form.clear_data.data:  # ************************************************************************** test this
            cursor = conn.cursor()
            cursor.execute('DELETE FROM transactions, charts, notes, input input WHERE userID =' + str(userid) + ';')
            flash('All user financial information successfully removed.', category='alert-success')
    return render_template('dashboard.html', title='Dashboard', form=form, chart_html=html)


def generate_chart_raw(uid):
    df = pd.read_sql(con=conn, sql='SELECT date, description, category, amount FROM transactions WHERE userID='+str(uid)+';')
    fig = go.Figure(data=[go.Table(header=dict(values=list(df.columns), fill_color='paleturquoise', align='left'),
                                   cells=dict(values=[df.date, df.description, df.category, df.amount], fill_color='lavender', align='left'))])
    fig.show()
    return fig

def generate_chart_table(uid):
    df = pd.read_sql(con=conn, sql='SELECT date, description, category, amount FROM transactions WHERE userID='+str(uid)+';')
    html = df.to_html()
    return html

def generate_chart_pie(uid):
    df = pd.read_sql(con=conn, sql="SELECT category, amount FROM transactions WHERE userID="+str(uid)+";")
    #df = df.set_index('category', drop=False).groupby((['category', 'amount'])).sum(axis=0)
    df = df.groupby(['category']).sum(axis=0)
    df['amount'] = df['amount'].abs()
    a = df['amount'].tolist()
    c = df.index.tolist()
    fig = go.Figure(data=[go.Pie(labels=c, values=a)])
    fig.show()


def generate_chart_bar(uid):
    df = pd.read_sql(con=conn, sql="SELECT date, amount FROM transactions WHERE userID="+str(uid)+";")
    df['amount'] = df['amount'].abs()
    df = df.groupby(['date']).sum(axis=0)
    x = df.index.tolist()
    y = df['amount'].tolist()
    fig = go.Figure(data=[go.Bar(y=y, x=x)])
    fig.show()


def generate_chart_progress(uid):  # line graph
    df = pd.read_sql(con=conn, sql="SELECT date, amount FROM transactions WHERE userID=" + str(uid) + ";")
    df['amount'] = df['amount'].abs()
    df = df.groupby(['date']).sum(axis=0)
    x = df.index.tolist()
    y = df['amount'].tolist()
    fig = go.Figure(data=[go.Scatter(y=y, x=x)])
    fig.show()


def get_user_trans(uid):
    cursor = conn.cursor()
    cursor.execute("SELECT amount FROM transactions WHERE userID="+str(uid)+";")
    transactions = cursor.fetchall()
    cursor.close()
    return transactions


def get_user_trans_cat(uid, cat):
    cursor = conn.cursor()
    cursor.execute("SELECT amount FROM transactions WHERE userID="+str(uid)+" AND category="+cat+";")
    transactions = cursor.fetchall()
    cursor.close()
    return transactions


def get_total_trans(uid, total=0):
    transactions = get_user_trans(uid=uid)
    for x in transactions:
        total += transactions[x]
    return total


def has_data(uid, conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions WHERE userID = '+str(uid)+';')
    if cursor.rowcount == 0:
        cursor.close()
        return False
    else:
        cursor.close()
        return True


def set_new_goal(new_goal):
    new_goal_message = "I am switching my current goal from " + current_user.goal + " to " + new_goal + "!"
    goal_note = Note(id=uuid1().time_low, date=datetime.now(), content=new_goal_message, userID=current_user.id)
    db.session.add(goal_note)
    db.session.commit()
    current_user.goal = new_goal
    flash(new_goal_message, category='alert-success')


def quick_note(note_content):
    note = Note(id=uuid1().time_low, author=current_user.username, date=datetime.now(), content=note_content, userID=current_user.id, title='New_Note_'+str(datetime.now()))
    db.session.add(note)
    db.session.commit()
    flash('Your note has been created!', 'success')
    return redirect(url_for('home'))


def color_negative_red(val):
    if isinstance(val, int):
        color = 'red' if val < 0 else 'black'
        return 'color: %s' % color

def highlight_max(s):
    is_max = s == s.min()
    return ['background-color: yellow' if v else '' for v in is_max]


@main.route("/note/new", methods=['GET', 'POST'])
@login_required
def new_note():
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(title=form.title.data, content=form.content.data, author=current_user.username, userID=current_user.id, date=datetime.now(), id=uuid1().time_low, img="/"+current_user.image)
        db.session.add(note)
        db.session.commit()
        flash('Your note has been created!', category='alert-success')
        return redirect(url_for('main.note', id=note.id))
    return render_template('create_note.html', title='New Note', form=form, legend='New Note')


@main.route("/note/<int:id>")
def note(id):
    note = Note.query.get_or_404(id)
    return render_template('note.html', title=note.title, note=note)


@main.route("/note/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_note(id):
    note = Note.query.get_or_404(id)
    if note.author != current_user:
        os.abort(403)
    form = NoteForm()
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        db.session.commit()
        flash('Your note has been updated!', 'success')
        return redirect(url_for('main.note', id=note.id))
    elif request.method == 'GET':
        form.title.data = note.title
        form.content.data = note.content
    return render_template('create_note.html', title='Update Note', form=form, legend='Update Note')


@main.route("/note/<int:id>/delete", methods=['POST'])
@login_required
def delete_note(id):
    note = Note.query.get_or_404(id)
    if note.author != current_user.username:
        os.abort()  # 403
    db.session.delete(note)
    db.session.commit()
    flash('Your note has been deleted!', category='alert-success')
    return render_template('home.html', title='Home')



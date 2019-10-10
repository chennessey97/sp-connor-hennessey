from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
#from forms import RegistrationForm, LoginForm
from forms import RegistrationForm, LoginForm

app = Flask(__name__)  # name of module
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'root:pass@localhost:3306'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    profile = db.relationship('Profile', backref='user_id', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_id'), nullable=False)


# Web Pages:
@app.route('/')  # Root/Home page
@app.route("/home", methods=['GET', 'POST'])  # Root/Home page
def home():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('home.html', title='Home', form=form)


@app.route("/about")  # about page
def about():
    return render_template('about.html', title='About')


@app.route("/profile")  # about page
def profile():
    return render_template('profile.html', title='User Profile')


@app.route("/dashboard")  # about page
def dashboard():
    return render_template('dashboard.html', title='Dashboard')


@app.route("/data")  # about page
def data():
    return render_template('data.html', title='User Data')


# login pages:
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@dough.com' and form.password.data == 'pass':
            flash('You have been logged in!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run()

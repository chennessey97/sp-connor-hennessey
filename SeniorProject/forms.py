import wtforms
from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired, Optional
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from SeniorProject.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=100)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    remember = BooleanField('Remember Me')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is in use. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is in use. Please choose a different one.')

GOALS=[(0, 'Select Goal'), (.05, '5%'), (.10, '10%'), (.15, '15%'), (.20, '20%'),
       (.25, '25%'), (.30, '30%'), (.35, '35%'), (.40, '40%'), (.45, '45%'),
       (.50, '50%'), (.55, '55%'), (.60, '60%'), (.65, '65%'), (.70, '70%'), (.75, '75%'), ]
class SetGoal(FlaskForm):
    set_goal = SelectField(label='Set Goal', default='Select Goal', choices=GOALS)


VIEWS = [('none', 'Select View'), ('data_view', 'View Raw Table'), ('type_view', 'View By Category'),
         ('all_spending_view', 'View All Spending'), ('progress_view', 'View Goal Progress')]
class DataView(FlaskForm):
    data_views = SelectField(label='View Data', default='Select View', choices=VIEWS)


class DataTable(FlaskForm):
    #set_goal = SelectField(label='Set Goal', default='Select Goal', choices=GOALS)
    data_view = BooleanField("Raw Data", validators=[Optional()])
    type_view = BooleanField("By Category", validators=[Optional()])
    all_spending_view = BooleanField("All Spending", validators=[Optional()])
    progress_view = BooleanField("Goal Progress", validators=[Optional()])
    clear_data = BooleanField('Clear All Data', validators=[Optional()])
    submit = SubmitField('Submit')


class NoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class Filter(FlaskForm):
    label = 'Filter Posts'
    filter = SelectField('Filter Posts', default='all_posts', choices=
    [('all_posts', 'All Posts'),
     ('my_posts', 'My Posts'),
     ('suggestions', 'Suggestions'),
     ('other_posts', 'Other Posts')])
    submit = SubmitField('Filter')

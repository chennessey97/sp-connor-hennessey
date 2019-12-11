from flask import Flask, flash, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
#from pysqlcipher3 import dbapi2 as sqlite
# import os import   urllib.request   from werkzeug.utils import secure_filename   import pandas as pd   from pandas import ExcelWriter, ExcelFile

db = SQLAlchemy()  # db = SQLAlchemy(app)

def create_app():
    app = Flask(__name__)  # name of module
    app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    db.init_app(app)

    UPLOAD_FOLDER = 'C:/Users/Connor/PycharmProjects/sp-connor-hennessey/SeniorProject/uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    login_manager = LoginManager(app)  # ()
    login_manager.login_view = 'main.login'  # 'auth.login'
    login_manager.init_app(app)
    # login_manager.login_message_category = 'info'  # necessary?
    # ******************* need to find a way to save uploaded files ****************************



    # blueprint for auth routes in our app
    from SeniorProject.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from SeniorProject.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))




    return app




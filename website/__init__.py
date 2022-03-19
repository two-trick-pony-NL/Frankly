from flask import Flask, flash 
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from configparser import ConfigParser
from sqlalchemy import true

db = SQLAlchemy()
config = ConfigParser()
config.read('Env_Settings.cfg')
token = config.get('SECRET_KEY', 'Session_Key')
mysqlusername = config.get('mysqlusername', 'mysqlusername')
mysqlpassword = config.get('mysqlpassword', 'mysqlpassword')

#Initializes the app and connects to the SQL database. For development there is also a SQLITE server available. 
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = token
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+mysqlusername+':'+mysqlpassword+'@petervandoorn.com/grapevine_database'
    db.init_app(app)

#Importing the views for routing. Views has general navigation, auth handles login in, and signup and payment handles all payment processes.
    from .views import views
    from .auth import auth
    from .payments import payments

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(payments, url_prefix="/")

    from .models import User, Post, Comment, Like
    #This function creates a new database if none exists and updates tables if those are updated in the models
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
        db.create_all(app=app)
        print("Connected to SQL database!")

from flask import Flask, flash 
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from configparser import ConfigParser

db = SQLAlchemy()
DB_NAME = "database.db"


config = ConfigParser()
config.read('Env_Settings.cfg')
token = config.get('SECRET_KEY', 'Session_Key')
mysqlusername = config.get('mysqlusername', 'mysqlusername')
mysqlpassword = config.get('mysqlpassword', 'mysqlpassword')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = token
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+mysqlusername+':'+mysqlpassword+'@petervandoorn.com/grapevine_database'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .payments import payments

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(payments, url_prefix="/")

    from .models import User, Post, Comment, Like
    #This function creates a new database if none exists
    #create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created database!")

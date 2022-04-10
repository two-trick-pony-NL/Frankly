from flask import Flask, flash 
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from configparser import ConfigParser
from sqlalchemy import true
from apilytics.flask import apilytics_middleware
from flask_migrate import Migrate



db = SQLAlchemy()
config = ConfigParser()
config.read('Env_Settings.cfg')
token = config.get('SECRET_KEY', 'Session_Key')
mysqlusername = config.get('mysqlusername', 'mysqlusername')
mysqlpassword = config.get('mysqlpassword', 'mysqlpassword')
apilyticskey = config.get('apilyticskey', 'apilyticskey')

#Initializes the app and connects to the SQL database. For development there is also a SQLITE server available. 
def create_app():
    app = Flask(__name__)
    #This next line allows for analytics to be sent to Apilytics so we can track server performance. 
    app = apilytics_middleware(app, api_key=apilyticskey)
    app.config['SECRET_KEY'] = token
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+mysqlusername+':'+mysqlpassword+'@petervandoorn.com/grapevine_database'
    db.init_app(app)
    migrate = Migrate(app, db)

#Importing the views for routing. Views has general navigation, auth handles login in, and signup and payment handles all payment processes.
    from .views import views
    from .auth import auth
    from .payments import payments
    from .chats import chats
    from .messaging import messaging
    from .blog import blog
    from .legal import legal

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(payments, url_prefix="/")
    app.register_blueprint(chats, url_prefix="/")
    app.register_blueprint(messaging, url_prefix="/")
    app.register_blueprint(blog, url_prefix="/blog")
    app.register_blueprint(legal, url_prefix="/legal")

    from .models import User, Post, Comment, Like

#This seems not to be used. 
    #This function creates a new database if none exists and updates tables if those are updated in the models
    #create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

#This seems not to be used. 
#def create_database(app): 
 #       db.create_all(app=app)
 #       print("Connected to SQL database!")

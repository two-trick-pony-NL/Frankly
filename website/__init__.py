from flask import Flask, flash 
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from configparser import ConfigParser
from sqlalchemy import true
from apilytics.flask import apilytics_middleware
from flask_migrate import Migrate
from flask_mail import Mail, Message


db = SQLAlchemy()
mail = Mail()
config = ConfigParser()
config.read('Env_Settings.cfg')
token = config.get('SECRET_KEY', 'Session_Key')
mysqlusername = config.get('mysqlusername', 'mysqlusername')
mysqlpassword = config.get('mysqlpassword', 'mysqlpassword')
apilyticskey = config.get('apilyticskey', 'apilyticskey')
email_password = config.get('email_password', 'email_password')

#Initializes the app and connects to the SQL database. For development there is also a SQLITE server available. 
def create_app():
    app = Flask(__name__)
    #This next line allows for analytics to be sent to Apilytics so we can track server performance. 
    app = apilytics_middleware(app, api_key=apilyticskey)
    #Set secret token for encryption
    app.config['SECRET_KEY'] = token
    #Not tracking all modifications in our DB
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #Setting URL for the Database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+mysqlusername+':'+mysqlpassword+'@petervandoorn.com/frankly_database'
    #Connecting Database to our app
    db.init_app(app)
    # configuration of mail
    
    app.config['MAIL_SERVER']='mail.franklyapp.nl'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'noreply@franklyapp.nl'
    app.config['MAIL_PASSWORD'] = email_password
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail.init_app(app)
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

    from .models import User, Post, Comment

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

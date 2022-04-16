from click import password_option
from flask import Blueprint, render_template, redirect, url_for, request, flash
from sqlalchemy import false
from . import db
from .models import User
from .qrgenerator import createQR
from configparser import ConfigParser

from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re
import phonenumbers
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from authlib.jose import jwt

config = ConfigParser()
config.read('Env_Settings.cfg')
secretkey = config.get('SECRET_KEY', 'Session_Key')

# These regexes are used to check whether the passwords, email addresses and usernames are valid during signup. 
regexemail = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
regexpassword = re.compile('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')                     
rexexusername = re.compile("^[a-zA-Z0-9_]*$")
regexphonenumber = re.compile("(^\+[0-9]{2}|^\+[0-9]{2}\(0\)|^\(\+[0-9]{2}\)\(0\)|^00[0-9]{2}|^0)([0-9]{9}$|[0-9\-\s]{10}$)")

auth = Blueprint("auth", __name__)

#This function handles signin
@auth.route("/sign-in", methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                userID=user.id
                createQR(userID)
                return redirect(url_for('views.dashboard', user=current_user, username=user.username))
            else:
                flash("Password is incorrect.", category='danger')
        else:
            flash("e-mail address does not exist.", category='danger')

    return render_template("signin.html", user=current_user)    

#This function handles signup 
@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        phonenumber = request.form.get("phonenumber")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        option = request.form.get('option')
        customquestion0 = "How did you like our service?"
        customquestion1 = "What do you think we can improve?"
        customquestion2 = "is there anything else you'd like to tell us?"
        
# checking if user exists
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if option != "accepted":
            flash("Accept the terms and conditions to create an account", category="danger")
        if not re.fullmatch(regexemail, email):
            flash("This is not a valid email address", category="danger")
        if not re.fullmatch(regexphonenumber, phonenumber):
            flash("This is not a valid phonenumber -- Use the format +31612345678", category="danger")  
        elif len(phonenumber) < 6:
            flash("Phone number is too short ", category="danger")    
        elif email_exists:
            flash("This Email address is already in use, use another one or log in", category="danger")
        elif username_exists:
            flash("This username is already in use, pick another one", category="danger")
        elif not re.fullmatch(regexpassword, password1):
            flash("This is not a strong password, pick at least 8 charachters and use numbers and symbols", category="danger")
        elif password1 != password2:
            flash("Passwords do not match!", category="danger")
        elif len(username) < 3:
            flash("Username is too short - use at least 3 characters", "warning")
        elif not re.fullmatch(rexexusername, username): 
            flash("You can only use letters numbers and _ in your username, try something else.", "warning")
        elif len(password1) < 6:
            flash("Password is too short -- Use at least 8 characters, Numbers and Symbols for a strong password", category="danger")
        elif len(email) < 4:
            flash("Email address is invalid.", category="danger")
        else:
            #formatting to international standard number
            my_number = phonenumbers.parse(phonenumber, "NL")
            phonenumberformatted = phonenumbers.format_number(my_number, phonenumbers.PhoneNumberFormat.E164)

            new_user = User(email=email, phonenumber=phonenumberformatted, haspaid = 1, customquestion0 = customquestion0, customquestion1 = customquestion1, customquestion2 = customquestion2, isadmin = False, username=username, userpublicname=username,  password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created succesfully, welcome!", "success")
            userID = current_user.id
            print("User created:")
            print(userID)
            createQR(userID)
            return redirect(url_for('views.dashboard', username=username))

    return render_template("signup.html", user=current_user)



#Handles the logout function
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You Logged out -- See you soon! !", category="success")
    print("User logged out")
    return redirect(url_for("views.home"))

#Creates and validates tokens for password reset
@auth.route("/forgot-password", methods=['GET', 'POST'])
def forgotpassword():
    if request.method == 'GET':    # On get request we just redirect to the forgotpassword page if the user is logged out 
        if current_user.is_authenticated:
            return redirect(url_for('views.home'))
        return render_template('forgotpassword.html', user='none')
    if request.method == 'POST': #On post we check if the email is a valid email regex and if we know this emailaddress
        email = request.form.get("email")
        email_exists = User.query.filter_by(email=email).first()
        print(email_exists)
        if not re.fullmatch(regexemail, email):
            flash("This is not a valid email address", category="danger")
        if email_exists:
            print(email)
            print("WE should send the reset link to that email address")
            token = email_exists.id
            get_reset_token(token)

        else:
            print("we do not know this email address")
            pass
    flash("If we know this email address, then you received an email to reset your password", category='success')
    return render_template('forgotpassword.html', user='none')


@auth.route("/reset-password/<token>")
def resetpassword(token):
    if request.method == 'GET':    # On get request we just redirect to the forgotpassword page if the user is logged out 
        if current_user.is_authenticated:
            return redirect(url_for('views.home'))
        return render_template('resetpassword.html', user='none')
    return


#This function generates a password reset token so we can safely execute password resets
def get_reset_token(token):
    header = {'alg': 'RS256'}
    payload = {'user_id': token}
    key = secretkey
    s = jwt.encode(header,payload, key)
    return s

#This function validates reset tokens, and returns the userID that we encrypted within the token
@staticmethod
def verify_reset_token(token):
    s = Serializer(token)
    try: 
        user_id = s.loads(token)['user_id']
    except:
        return None
    return User.query.get(user_id)
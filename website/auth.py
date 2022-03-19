from flask import Blueprint, render_template, redirect, url_for, request, flash
from sqlalchemy import false
from . import db
from .models import User
from .qrgenerator import createQR
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re

# These regexes are used to check whether the passwords, email addresses and usernames are valid during signup. 
regexemail = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
regexpassword = re.compile('[A-Za-z0-9@#$%^&+=]{8,}')
rexexusername = re.compile("^[a-zA-Z0-9_]*$")

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
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        option = request.form.get('option')


        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if option != "accepted":
            flash("Accept the terms and conditions to create an account", category="danger")
        if not re.fullmatch(regexemail, email):
            flash("This is not a valid email address", category="danger")
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
            new_user = User(email=email, username=username, password=generate_password_hash(
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

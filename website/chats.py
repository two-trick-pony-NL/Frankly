from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import Post, User, Comment, Like
from . import db

chats = Blueprint("chats", __name__)

#Here we ask the second question on the GET request and on Post we receive the second answer
@chats.route("/step2",methods=['GET', 'POST'])
def step2():
    answer1 = request.args.get('text')
    ThisPost = request.args.get('ThisPost')
    user = request.args.get('user')
    user = User.query.filter_by(username=user).first()
    print(user)
    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Comment cannot be empty.', category='warning')
        else:
            post = ThisPost
            
            if post:
                comment = Comment(
                    text=text, author=user.id, post_id=ThisPost)
                db.session.add(comment)
                db.session.commit()

                #return render_template('chats/chatquestion1.html', text = text, ThisPost=ThisPost)
                answer2 = text
                return redirect(url_for('chats.step3', ThisPost=ThisPost, answer2 =answer2 , answer1 =answer1, user=user.id, username=user.username, question0 = user.customquestion0, question1 = user.customquestion1, question2 = user.customquestion2))

    return render_template("chats/chatquestion2_new.html", user=user.id, answer1=answer1, username=user.username, question0 = user.customquestion0, question1 = user.customquestion1, question2 = user.customquestion2)  

#Here we ask the third question on the GET request and on Post we receive the third answer

@chats.route("/step3",methods=['GET', 'POST'])
def step3():
    answer1 = request.args.get('answer1')
    answer2 = request.args.get('answer2')
    ThisPost = request.args.get('ThisPost')
    user = request.args.get('user')
    user = User.query.filter_by(id=user).first()
    username = user.username
    print(user)
    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Comment cannot be empty.', category='warning')
        else:
            post = ThisPost
            
            if post:
                comment = Comment(
                    text=text, author=user.id, post_id=ThisPost)
                db.session.add(comment)
                db.session.commit()

                #return render_template('chats/chatquestion1.html', text = text, ThisPost=ThisPost)
                answer3 = text
                return redirect(url_for('chats.thanks', answer1 = answer1, answer2 = answer2,answer3= answer3, username=username, ThisPost=ThisPost, user=user, question0 = user.customquestion0, question1 = user.customquestion1, question2 = user.customquestion2))     
    return render_template("chats/chatquestion3_new.html", user=user, username=user.username, answer1=answer1,answer2=answer2, question0 = user.customquestion0, question1 = user.customquestion1, question2 = user.customquestion2)  

 
@chats.route("/thanks",methods=['GET', 'POST'])
def thanks():
    answer1 = request.args.get('answer1')
    answer2 = request.args.get('answer2')
    answer3 = request.args.get('answer3')
    ThisPost = request.args.get('ThisPost')
    username = request.args.get('username')
    #user = request.args.get('user')
    user = User.query.filter_by(username=username).first()
    print(user)
    return render_template("chats/thanks_new.html", username = username, answer1=answer1, answer2=answer2, answer3=answer3, question0 = user.customquestion0, question1 = user.customquestion1, question2 = user.customquestion2)    


@chats.route("/question-answered1/<post_id>", methods=['GET','POST'])
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='warning')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='warning')
    return redirect(url_for('views.dashboard', user=user))    
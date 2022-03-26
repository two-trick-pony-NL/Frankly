from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import Post, User, Comment, Like
from . import db

chats = Blueprint("chats", __name__)

"""
#Here we send the user to the chat windown if the method is get, and on post we receive the first answer
@chats.route("/create-post", methods=['GET', 'POST'])
def create_post():
    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Post cannot be empty', category='warning')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.dashboard'))

    return render_template('chats/create_post.html', user=current_user.username)
"""
#Here we ask the second question on the GET request and on Post we receive the second answer
@chats.route("/step2",methods=['GET', 'POST'])
def step2():
    answer1 = request.args.get('text')
    ThisPost = request.args.get('ThisPost')
    user = request.args.get('user')

    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Comment cannot be empty.', category='warning')
        else:
            post = ThisPost
            
            if post:
                comment = Comment(
                    text=text, author=user, post_id=ThisPost)
                db.session.add(comment)
                db.session.commit()

                #return render_template('chats/chatquestion1.html', text = text, ThisPost=ThisPost)
                answer2 = text
                return redirect(url_for('chats.step3', ThisPost=ThisPost, answer2 =answer2 , answer1 =answer1, user=user))

    return render_template("chats/chatquestion2.html", user=user, answer1=answer1)  

#Here we ask the third question on the GET request and on Post we receive the third answer

@chats.route("/step3",methods=['GET', 'POST'])
def step3():
    answer1 = request.args.get('answer1')
    answer2 = request.args.get('answer2')
    ThisPost = request.args.get('ThisPost')
    user = request.args.get('user')

    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Comment cannot be empty.', category='warning')
        else:
            post = ThisPost
            
            if post:
                comment = Comment(
                    text=text, author=user, post_id=ThisPost)
                db.session.add(comment)
                db.session.commit()

                #return render_template('chats/chatquestion1.html', text = text, ThisPost=ThisPost)
                answer3 = text
                return redirect(url_for('chats.thanks', answer1 = answer1, answer2 = answer2,answer3= answer3, ThisPost=ThisPost, user=user))     
    return render_template("chats/chatquestion3.html", user=user, answer1=answer1,answer2=answer2)  

 
@chats.route("/thanks",methods=['GET', 'POST'])
def thanks():
    answer1 = request.args.get('answer1')
    answer2 = request.args.get('answer2')
    answer3 = request.args.get('answer3')
    ThisPost = request.args.get('ThisPost')
    user = request.args.get('user')
    return render_template("chats/thanks.html", answer1=answer1, answer2=answer2, answer3=answer3)    


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
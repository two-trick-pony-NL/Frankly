from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import Post, User, Comment, Like
from . import db

chats = Blueprint("chats", __name__)



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

## DO replace the curren_user attribute with the author of the post. Otherwise you have to be signed in to post. 

@chats.route("/step1",methods=['GET', 'POST'])
def step1():
    previoustext = request.args.get('text')
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

                flash('Feedback received!', category='success')
                #return render_template('chats/chatquestion1.html', text = text, ThisPost=ThisPost)
                return redirect(url_for('chats.step2', text1 = text, ThisPost=ThisPost , previoustext =previoustext, user=user))

    return render_template("chats/chatquestion1.html", user=current_user.username, previoustext=previoustext)  


@chats.route("/step2",methods=['GET', 'POST'])
def step2():
    previoustext = request.args.get('previoustext')
    text1 = request.args.get('text1')
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

                flash('Feedback received!', category='success')
                #return render_template('chats/chatquestion1.html', text = text, ThisPost=ThisPost)
                return redirect(url_for('chats.step3', text2 = text, text1 = text1, ThisPost=ThisPost, user=user))     
    return render_template("chats/chatquestion2.html", user=current_user.username, previoustext=previoustext)  

@chats.route("/step3",methods=['GET', 'POST'])
def step3():
    previoustext = request.args.get('previoustext')
    text1 = request.args.get('text1')
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

                flash('Feedback received!', category='success')
                #return render_template('chats/chatquestion1.html', text = text, ThisPost=ThisPost)
                return redirect(url_for('chats.thanks'))     
    return render_template("chats/chatquestion3.html", user=current_user.username, previoustext=previoustext)  


@chats.route("/thanks")
def thanks():
    return render_template("chats/thanks.html", user=current_user.username)    


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
    return redirect(url_for('views.dashboard', username = current_user.username))    
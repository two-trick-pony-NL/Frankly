from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, send_file
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like
import os
from . import db

views = Blueprint("views", __name__)

#this file renders navigation on the page. All endpoints and logic are here. See auth and payment for endpoints on those topics
#Renders the homepage and the / redirect
@views.route("/")
@views.route("/home")
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)


#Renders the userdashboard requires a username to select the correct user dashboard
@views.route("/dashboard/<username>", methods=['GET', 'POST'])
@login_required
def dashboard(username):
    #If it is a post then the user is updating his settings, and the page does not need rendering. 
    if request.method == 'POST':
        FirstCustomQuestion = request.form.get("FirstCustomQuestion")
        FollowUpQuestion1 = request.form.get("FollowUpQuestion1")
        FollowUpQuestion2 = request.form.get("FollowUpQuestion2")

        user = User.query.filter_by(username=username).first()
        if len(FirstCustomQuestion) > 0:
            user.customquestion0 =  FirstCustomQuestion
            db.session.commit()
            print("First Question updated") 
        if len(FollowUpQuestion1) > 0:
            user.customquestion1 =  FollowUpQuestion1
            db.session.commit()
            print("Second Question updated")
        if len(FollowUpQuestion2) > 0:
            user.customquestion2 =  FollowUpQuestion2
            db.session.commit()
            print("Third Question updated")

#Get requests just load the page with the regular logic
    user = User.query.filter_by(username=username).first()
    userID = user.id
    userID = str(userID)
    urlPromotorQR = userID+"_promotor.png"
    urlNeutralQR = userID+"_neutral.png"
    urlDetractorQR = userID+"_detractor.png"


    if not user:
        flash("No user with that username exists, try creating a new account", category='info')
        return redirect(url_for('views.home'))

#Making sure the logged in user is the owner of the dashboard
    if user != current_user:
        flash("You have no access to this page" , category="warning")    
        return redirect(url_for('views.home'))
#Sorting Posts newest first       
    posts = Post.query.filter_by(author=user.id).order_by(Post.date_created.desc())
    userID = str(current_user.id)
    QRCodeURL = "static/qrcodes/User_"+userID+"_promotor.png"
    #Collecting all the responses filtered by Happy, neutral and Unhappy
    nmbr_happy_users = Post.query.filter(
        Post.author.like(user.id),
        Post.rating.like(3)
        ).count()

    nmbr_medium_users = Post.query.filter(
        Post.author.like(user.id),
        Post.rating.like(2)
        ).count()

    nmbr_unhappy_users = Post.query.filter(
        Post.author.like(user.id),
        Post.rating.like(1)
        ).count()    
    #Adding up all responses    
    totalresponses = nmbr_happy_users+nmbr_medium_users+nmbr_unhappy_users
    #Making a dataframe out of the filtered responses so we an draw the graphs in the dashboard
    data = [
        ("Happy Users", nmbr_happy_users),
        ("Neutral Users", nmbr_medium_users),
        ("Unhappy Users", nmbr_unhappy_users)
    ]
    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    #Calculating the % of happy users for the donut chart and rounding it up to the next whole number. If total responses is 0 we'll return 0 so we don't devide by 0. 
    try:
        percentagehappyusers = round((nmbr_happy_users/totalresponses)*100)
        percentageneutralusers = round((nmbr_medium_users/totalresponses)*100)
        percentageunhappyusers = round((nmbr_unhappy_users/totalresponses)*100)
    except:
        percentagehappyusers = 0      
        percentageneutralusers = 0
        percentageunhappyusers = 0

    piedata = [
        ("Percentage Happy Users",percentagehappyusers ),
        ("Percentage Neutral Users",percentageneutralusers ),
        ("Percentage Unhappy Users",percentageunhappyusers ),
    ]
    percentagelabels = [row[0] for row in piedata]
    percentagevalues = [row[1] for row in piedata]

    #NPS style calculation - again trying to avoid deviding by zero
    try:
        grapevinescore = round(((nmbr_happy_users/totalresponses)-(nmbr_unhappy_users/totalresponses))*100)
    except: 
        grapevinescore = 0    
    return render_template("dashboard.html", percentagelabels=percentagelabels, percentagevalues=percentagevalues, urlPromotorQR=urlPromotorQR, urlNeutralQR=urlNeutralQR,urlDetractorQR=urlDetractorQR,  grapevinescore=grapevinescore, totalresponses=totalresponses, nmbr_happy_users=nmbr_happy_users, nmbr_medium_users=nmbr_medium_users, nmbr_unhappy_users=nmbr_unhappy_users,QRCodeURL=QRCodeURL, user=current_user, posts=posts, username=username, labels=labels, values=values)
  
@views.route("/settings/<username>")
@login_required
def settings(username):
    user = User.query.filter_by(username=username).first()
    #Making sure the logged in user is the owner of the dashboard
    if user != current_user:
        flash("You have no access to this page" , category="warning")    
        return redirect(url_for('views.home'))
    return render_template("settings.html", user=current_user, username=username,)  

@views.route("/createassets/<username>")
@login_required
def createassets(username):
    user = User.query.filter_by(username=username).first()
    userID = user.id
    userID = str(userID)
    urlPromotorQR = userID+"_promotor.png"
    urlNeutralQR = userID+"_neutral.png"
    urlDetractorQR = userID+"_detractor.png"
    #Making sure the logged in user is the owner of the dashboard
    if user != current_user:
        flash("You have no access to this page" , category="warning")    
        return redirect(url_for('views.home'))
    return render_template("createassets.html", user=current_user,urlDetractorQR=urlDetractorQR,urlNeutralQR=urlNeutralQR, urlPromotorQR= urlPromotorQR, username=username,)    


@views.route("/send-feedback/<user>/<rating>", methods=['GET', 'POST'])
def send_feedback(user, rating):
    user = User.query.filter_by(id=user).first()
    print(user)
    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Post cannot be empty', category='warning')
        else:
            print(user)
            post = Post(text=text, rating=rating, author=user.id)
            db.session.add(post)
            db.session.commit()
            LastPost = Post.query.filter_by(text=text).first()
            ThisPost = LastPost.id
            ThisPost = str(ThisPost)
            print(ThisPost)
            return redirect(url_for('chats.step2', text = text, ThisPost=ThisPost, user=user.username, question0 = user.customquestion0, question1 = user.customquestion1, question2 = user.customquestion2))

    return render_template('/chats/chatquestion1.html', username=user.username, question0 = user.customquestion0, question1 = user.customquestion1, question2 = user.customquestion2)    


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='warning')
    elif current_user.id != post.id:
        flash('You do not have permission to delete this post.', category='warning')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('views.home'))


@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='warning')
        return redirect(url_for('views.dashboard', username=username))

    posts = user.posts
    return render_template("posts.html", user=current_user, posts=posts, username=username)


@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
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


@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='warning')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='warning')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.dashboard', username=username))


@views.route("/like-post/<post_id>", methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(
        author=current_user.id, post_id=post_id).first()

    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)})

@views.route('/downloadQR/<userid>/promotor')
@login_required
def downloadFilePromotor (userid):
    qr3 = 'User_'+userid+'_promotor.png'
    file3 = "static/qrcodes/"+qr3
    return(send_file(file3, as_attachment=True)) 

@views.route('/downloadQR/<userid>/neutral')
@login_required
def downloadFileNeutral (userid):
    qr2 = 'User_'+userid+'_neutral.png'
    file2 = "static/qrcodes/"+qr2
    return(send_file(file2, as_attachment=True)) 

@views.route('/downloadQR/<userid>/detractor')
@login_required
def downloadFileDetractor (userid):
    qr1 = 'User_'+userid+'_detractor.png'
    file1 = "static/qrcodes/"+qr1
    return(send_file(file1, as_attachment=True)) 
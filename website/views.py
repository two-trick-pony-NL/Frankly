from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like
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
@views.route("/dashboard/<username>")
@login_required
def dashboard(username):



    user = User.query.filter_by(username=username).first()

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
        ("Medium Users", nmbr_medium_users),
        ("Unhappy Users", nmbr_unhappy_users)
    ]
    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    #NPS style calculation
    try:
        grapevinescore = round(((nmbr_happy_users/totalresponses)-(nmbr_unhappy_users/totalresponses))*100)
    except: 
        grapevinescore = 0    
    return render_template("dashboard.html", grapevinescore=grapevinescore, totalresponses=totalresponses, nmbr_happy_users=nmbr_happy_users, nmbr_medium_users=nmbr_medium_users, nmbr_unhappy_users=nmbr_unhappy_users,QRCodeURL=QRCodeURL, user=current_user, posts=posts, username=username, labels=labels, values=values)
  
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

@views.route("/thanks")
def thanks():
    return render_template("thanks.html", user=current_user)
      
@views.route("/demo")
def demo():
    return render_template("demo.html", user=current_user)

@views.route("/create-post", methods=['GET', 'POST'])
@login_required
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

    return render_template('create_post.html', user=current_user)

@views.route("/send-feedback/<user>/<rating>", methods=['GET', 'POST'])
def send_feedback(user, rating):
    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Post cannot be empty', category='warning')
        else:
            post = Post(text=text, rating=rating, author=user)
            db.session.add(post)
            db.session.commit()
            flash('Feedback received!', category='success')
            return redirect(url_for('views.thanks'))

    return render_template('create_post.html', user=current_user)    


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

    return redirect(url_for('views.dashboard'))


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

    return redirect(url_for('views.dashboard'))


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

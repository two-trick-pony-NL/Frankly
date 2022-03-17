from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like
from . import db

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)


@views.route("/dashboard/<username>")
@login_required
def dashboard(username):
    data = [
        ("01-01-2021", 25,40),
        ("01-02-2021", 34,40),
        ("01-03-2021", 12,40),
        ("01-04-2021", 17,40),
        ("01-05-2021", 60,40),
        ("01-06-2021", 45,40)
    ]
    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    target = [row[2] for row in data]

    user = User.query.filter_by(username=username).first()

    if not user:
        flash("No user with that username exists, try creating a new account", category='info')
        return redirect(url_for('views.home'))

#Making sure the logged in user is the owner of the dashboard
    if user != current_user:
        flash("You have no access to this page" , category="warning")    
        return redirect(url_for('views.home'))
#Sorting Posts newest first
    #posts = user.posts
    
    print(user)    
    posts = Post.query.filter_by(author=user.id).order_by(Post.date_created.desc())
    print(username)
    userID = str(current_user.id)
    QRCodeURL = "static/qrcodes/User_"+userID+"_promotor.png"
    print(QRCodeURL)
    return render_template("dashboard.html", QRCodeURL=QRCodeURL, user=current_user, posts=posts, username=username, labels=labels, values=values, target=target)
  
@views.route("/settings")
@login_required
def settings():
    return render_template("settings.html", user=current_user)

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

@views.route("/send-feedback/<user>/<nps>", methods=['GET', 'POST'])
def send_feedback(user, nps):
    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Post cannot be empty', category='warning')
        else:
            post = Post(text=text, nps=nps, author=user)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
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

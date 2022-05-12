from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, send_file, session
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like
from configparser import ConfigParser
from . import db

#fetching credentials used on this page
config = ConfigParser()
config.read('Env_Settings.cfg')
# Getting the number of responses you need before you have to pay
free_responses = config.get('free_responses', 'free_responses')
free_responses = int(free_responses)

views = Blueprint("views", __name__)

#this file renders navigation on the page. All endpoints and logic are here. See auth and payment for endpoints on those topics
#Renders the homepage and the / redirect
@views.route("/")
@views.route("/home")
def home():
    posts = Post.query.all()
    print("homepage was loaded")
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
        userpublicname = request.form.get("userpublicname")
        userlogo = request.form.get("userlogo")

        user = User.query.filter_by(username=username).first()
        if len(FirstCustomQuestion) > 0:
            user.customquestion0 =  FirstCustomQuestion
            db.session.commit()
            
        if len(FollowUpQuestion1) > 0:
            user.customquestion1 =  FollowUpQuestion1
            db.session.commit()
            
        if len(FollowUpQuestion2) > 0:
            user.customquestion2 =  FollowUpQuestion2
            db.session.commit()

        if len(userpublicname) > 0:
            user.userpublicname =  userpublicname
            db.session.commit()

        if len(userlogo) > 0:
            user.userlogo =  userlogo
            db.session.commit()    
            

#Get requests just load the page with the regular logic
    user = User.query.filter_by(username=username).first()
    try: #Addint a try/Except block here as I had ver weird error messages in this section
        haspaid = bool(user.haspaid)
        userID = user.id
        userID = str(userID)
        urlPromotorQR = userID+"_promotor.png"
        urlNeutralQR = userID+"_neutral.png"
        urlDetractorQR = userID+"_detractor.png"
    except:
        haspaid = 1    
    
    if not user:
        flash("No user with that username exists, try creating a new account", category='info')
        return redirect(url_for('views.home'))

#Making sure the logged in user is the owner of the dashboard
    if user != current_user:
        flash("You have no access to this page" , category="warning")    
        return redirect(url_for('views.home'))
#Sorting Posts newest first
    #Setting up pagination
    page = request.args.get('page', 1, type=int)
    #First getting all posts and ordering decendign order
    posts = Post.query.filter_by(author=user.id).order_by(Post.date_created.desc())
    #This section fetches common words from the session. We calculate these in the sign-in function. So we only have to do it 1x
    NegativeWordLabels = session.get('NegativeWordLabels')
    NegativeWordValues = session.get('NegativeWordValues')
    PositiveWordLabels = session.get('PositiveWordLabels')
    PositiveWordValues = session.get('PositiveWordValues')

    #Now breaking up the ordered list into pages
    posts = posts.paginate(page=page, per_page=5)       
    userID = str(current_user.id)
    #REnder the URL for the example QR code
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
    #Here we calculate what % of the free responses the user used. The modulus calculator sends back the remainder
    ModTotalpost = totalresponses % free_responses
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
        Franklyscore = round(((nmbr_happy_users/totalresponses)-(nmbr_unhappy_users/totalresponses))*100)
    except: 
        Franklyscore = 0    
    return render_template("dashboard.html",haspaid=haspaid, PositiveWordValues=PositiveWordValues, PositiveWordLabels=PositiveWordLabels, NegativeWordValues=NegativeWordValues, NegativeWordLabels=NegativeWordLabels,  page=page, ModTotalpost=ModTotalpost, percentagelabels=percentagelabels, percentagevalues=percentagevalues, urlPromotorQR=urlPromotorQR, urlNeutralQR=urlNeutralQR,urlDetractorQR=urlDetractorQR,  Franklyscore=Franklyscore, totalresponses=totalresponses, nmbr_happy_users=nmbr_happy_users, nmbr_medium_users=nmbr_medium_users, nmbr_unhappy_users=nmbr_unhappy_users,QRCodeURL=QRCodeURL, user=current_user, posts=posts, username=username, labels=labels, values=values)
  
  

@views.route("/send-feedback/<user>/<rating>", methods=['GET', 'POST'])
def send_feedback(user, rating):
    user = User.query.filter_by(id=user).first()
    totalposts = Post.query.filter(
        Post.author.like(user.id)).count()
    print(totalposts)
    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Post cannot be empty', category='warning')
        else:
            post = Post(text=text, rating=rating, author=user.id)
            db.session.add(post)
            db.session.commit()
            LastPost = Post.query.filter_by(text=text).first()
            ThisPost = LastPost.id
            ThisPost = str(ThisPost)
            #The free responses can be set from the env_settings file, and returns ModTotalPost which is used to determine when a user has to pay. I
            ModTotalpost = totalposts % free_responses
            print(ModTotalpost)
            print(text)
            # If ModTotalpost == 0 it means that you have reached that number, and then it will set the database that you'll have to pay.
            if totalposts < 50: #This line is added because the first response will also lead to modulus being 0 and thus trigger payment after just 1 response
                pass
            else:
                if ModTotalpost == 0:
                    user.haspaid =  0
                    print("#####THe payment was triggered")
                    db.session.commit()
                    ModTotalpost == 1
                else:
                    print("#####The payment was not triggered")
            return redirect(url_for('chats.step2', ModTotalpost=ModTotalpost, text = text, ThisPost=ThisPost, user=user.username, question0 = user.customquestion0, question1 = user.customquestion1, question2 = user.customquestion2))

    return render_template('/chats/chatquestion1.html', publicname=user.userpublicname, username=user.username, question0 = user.customquestion0, question1 = user.customquestion1, question2 = user.customquestion2)    


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='warning')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('views.dashboard', username = current_user.username))


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

    return redirect(url_for('views.dashboard', username = current_user.username))


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
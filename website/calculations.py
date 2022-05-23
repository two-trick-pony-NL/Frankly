from distutils.command.build_scripts import first_line_re
from flask import session
import itertools
from collections import Counter
from regex import P
from stop_words import get_stop_words
from .models import Post, User
from configparser import ConfigParser
from datetime import datetime



#This section of code creates a list of all the words used in posts by users, so we can draw a wordcloud.
# We do this on login so that we only have to do it 1x and store in in session from there on
#This is a list of local stopwords so we have some flexibility over words to exclude from the wordcount
config = ConfigParser()
config.read('Env_Settings.cfg')
localstopwords = config.get('localstopwords', 'localstopwords')



def calculatecommonwords(userID): #Function is called in the Auth script on signin
    PositivePosts = Post.query.filter_by(author=userID, rating=3).order_by(Post.date_created.desc())
    NegativePosts = Post.query.filter_by(author=userID, rating=1).order_by(Post.date_created.desc())
    wordcloudlistPositive = []
    wordcloudlistNegative = []
    #Removing stopwords so only important words remain   
    for post in PositivePosts: 
        wordcloudlistPositive.append(post.text.split())
        for comment in post.comments:   
            wordcloudlistPositive.append(comment.text.split()) 
    mergedwordcloudlist = list(itertools.chain(*wordcloudlistPositive))
    #Checking the words against known stopwords in EN and NL and making sure they are all lowercase with the .lower() function
    mergedwordcloudlist = [w.lower() for w in mergedwordcloudlist if not w in get_stop_words('english')]
    mergedwordcloudlist = [w.lower() for w in mergedwordcloudlist if not w in get_stop_words('dutch')]
    mergedwordcloudlist = [w.lower() for w in mergedwordcloudlist if not w in localstopwords]
    positivecommonwords = Counter(mergedwordcloudlist).most_common(10)

    #Here we convert the positive common words into values and labels and store these in the user session. 
    # The dashboard can later retrieve these details to draw graphs
    PositiveWordLabels = [row[0] for row in positivecommonwords]
    PositiveWordValues = [row[1] for row in positivecommonwords]
    session['PositiveWordLabels'] = PositiveWordLabels     
    session['PositiveWordValues'] = PositiveWordValues

    #Doing the same for negative posts
    for post in NegativePosts: 
        wordcloudlistNegative.append(post.text.split())
        for comment in post.comments:   
            wordcloudlistNegative.append(comment.text.split()) 
    mergedwordcloudlist = list(itertools.chain(*wordcloudlistNegative))
    mergedwordcloudlist = [w.lower() for w in mergedwordcloudlist if not w in get_stop_words('english')]
    mergedwordcloudlist = [w.lower() for w in mergedwordcloudlist if not w in get_stop_words('dutch')]
    mergedwordcloudlist = [w.lower() for w in mergedwordcloudlist if not w in localstopwords]
    negativecommonwords = Counter(mergedwordcloudlist).most_common(10)

    #Here we convert the positive common words into values and labels and store these in the user session. 
    # The dashboard can later retrieve these details to draw graphs
    NegativeWordLabels = [row[0] for row in negativecommonwords]
    NegativeWordValues = [row[1] for row in negativecommonwords]
    session['NegativeWordLabels'] = NegativeWordLabels     
    session['NegativeWordValues'] = NegativeWordValues


def calculatepostsovertime(userID):
    posts = Post.query.filter_by(author=userID).order_by(Post.date_created.desc())
    postcount = posts.count()
    if postcount < 1:
        print("There are 0 responses. Can't complete the calculation for posts over time. Skipping")
        session['timestamplabels'] = 0     
        session['countvalues'] = 0
        
    else:
        daterange = []
        for post in posts:
            datecreated = post.date_created.strftime("%Y-%m-%d")
            datecreated = str(datecreated)
            daterange.append(datecreated[0:10])
        commondates = Counter(daterange).most_common(1000)
        commondates.sort()
        now = datetime.now().strftime("%Y-%m-%d")
        first = commondates[0][0]

        print("Printing most common dates\n\n\n")
        print(commondates)
        print("stopped printing \n\n")
        timestamplabels = [row[0] for row in commondates]
        countvalues = [row[1] for row in commondates]
        session['timestamplabels'] = timestamplabels     
        session['countvalues'] = countvalues


def calculateseatsremaining():
    print(User.query.count())
    users_in_db = int(User.query.count())
    freeseats = 100
    remainingseats = freeseats - users_in_db
    print("Calculating how many seats we have left")
    print(remainingseats)
    return remainingseats


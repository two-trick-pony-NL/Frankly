from flask import session
import itertools
from collections import Counter
from stop_words import get_stop_words
from .models import Post
from configparser import ConfigParser

config = ConfigParser()
config.read('Env_Settings.cfg')
#This is a list of local stopwords so we have some flexibility over words to exclude from the wordcount
#They have to be all lowercase
localstopwords = config.get('localstopwords', 'localstopwords')

"""This section of code creates a list of all the words used in posts by users, so we can draw a wordcloud."""
# We do this on login so that we only have to do it 1x and store in in session from there on




def calculatecommonwords(userID):
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

    print("### Printing the results of word analysis")
    print("Negative words and count")
    print(NegativeWordLabels)  
    print(NegativeWordValues)   
    print("Positive words and count")
    print(PositiveWordLabels)
    print(PositiveWordValues)
    print(get_stop_words('dutch'))
    print(get_stop_words('english'))
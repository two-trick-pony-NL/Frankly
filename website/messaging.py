from audioop import mul
from curses import flash
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
from flask_login import login_required, current_user
from configparser import ConfigParser
from numpy import number
from twilio.rest import Client 
import os
from . import db
from . import mail
from .models import Post, User, Comment, Like
from flask_mail import Mail, Message
from datetime import datetime
#I'm using this template for emails: https://github.com/leemunroe/responsive-html-email-template


messaging = Blueprint("messaging", __name__)

#fetching credentials used on this page
config = ConfigParser()
config.read('Env_Settings.cfg')
#Twilio ID
account_sid = config.get('account_sid', 'account_sid')
auth_token = config.get('auth_token', 'auth_token')


#From here we have the Twillio Whatsapp integration
@messaging.route("/sendwhatsapp/<userid>/<phonenumber>")
@login_required
def SendWhatsapp(userid, phonenumber):
    user = User.query.filter_by(id=userid).first()
    client = Client(account_sid, auth_token) 
    phonenumber = str(phonenumber)
    promotorURL = str('\n\n\n😃 it’s great! > https://franklyapp.nl/send-feedback/'+userid+'/3')
    neutralURL = str('\n\n\n😐 it’s ok > https://franklyapp.nl/send-feedback/'+userid+'/2')
    detractorURL = str('\n\n\n🙄 it’s lacking > https://franklyapp.nl/send-feedback/'+userid+'/1')
    message = user.customquestion0
    sender= str(user.userpublicname)
    print(userid)
    message = client.messages.create( 
                                messaging_service_sid='MGcda453ae1d2d1f05cb4b8124367535b5', 
                                #To enable whatsapp add this line in again
                                #from_='whatsapp:+14155238886',  
                                body=message+promotorURL+neutralURL+detractorURL+"\n\n"+sender,      
                                #Replace this line to send whatsapp instead of text
                                #to='whatsapp:'+phonenumber
                                to=phonenumber
                            ) 
    print("Sending text message, message ID: ")
    print(message.sid)
    flash("Message sent to your phone, check your Whatsapp!", category='success')
    #return('', 204) 
    return redirect(url_for('views.dashboard', user=current_user, username=user.username))

#From here we have the email integration
@messaging.route("/SendMultipleEmail/<userid>/")
@login_required
def SendMultipleEmail(userid):
    user = User.query.filter_by(id=userid).first()
    multiplerecipients = request.args.get('multiplerecipients')
    multiplerecipients = multiplerecipients.split(", ")
    print("Starting batch email from user " + str(user))
    print(multiplerecipients)
    numberofmessages = len(multiplerecipients)
    failedmessages = []
    flash("Sending surveys to " + str(numberofmessages)+" recipients", category='info')
    for recipient in multiplerecipients:
      try:
        SendEmail(userid, recipient)
        
      except:
        flash("Message to " + str(recipient)+" failed. Is the email address correct?", category='danger')
        print("Message to " + str(recipient)+" failed.")
        failedmessages.append("Error")

    failedmessages = len(failedmessages)
    succesfulmessagessend = numberofmessages - failedmessages    
    flash("All surveys are sent! "+str(succesfulmessagessend)+" surveys were sent succesfully. \n" + str(failedmessages)+" surveys could not be send.", category='info')  
    print("\n\n"+str(succesfulmessagessend)+" emails sent. \nThere were " + str(failedmessages)+" errors.\n\n")     
    return redirect(url_for('views.dashboard', user=current_user, username=user.username))

#From here we have the email integration
@messaging.route("/sendemail/<userid>/<email>")
@login_required
def SendEmail(userid, email):
    user = User.query.filter_by(id=userid).first()
    publicusernamenospaces = user.userpublicname.replace(" ", "_")
    email = str(email)
    email = email.split()
    promotorURL = str('https://franklyapp.nl/send-feedback/'+userid+'/3')
    neutralURL = str('https://franklyapp.nl/send-feedback/'+userid+'/2')
    detractorURL = str('https://franklyapp.nl/send-feedback/'+userid+'/1')
    msg = Message(
                  user.customquestion0,
                  sender = str(publicusernamenospaces)+'@franklyapp.nl',
                  recipients = email
                )
    #msg.body = 'Welcome to Frankly! Your account was registered succesfully!'
    msg.html = render_template('emailtemplates/feedbacktemplate.html', question = user.customquestion0, userpublicname = user.userpublicname, promotorURL = promotorURL, neutralURL = neutralURL, detractorURL = detractorURL)
    mail.send(msg)
    print("Sending survey to" + str(email) + " from user: " +str(user))
    flash("Message sent to " + str(email), category='success')
    return redirect(url_for('views.dashboard', user=current_user, username=user.username))



#From here for the waiting list
@messaging.route("/getinvited", methods=['GET', 'POST'])
def getinvited():
  if request.method == 'GET':
    return render_template("getinvited.html", user = 'none', methods = ['GET', 'POST'])
  else:
    email = request.form.get("email")  
    email = str(email)
    print(email)
    msg = Message(
                'You are added to the frankly waiting list!',
                sender ='noreply@franklyapp.nl',
                recipients = [email, 'hello@franklyapp.nl']
               )
    msg.body = 'Welcome to Frankly! Your account was registered succesfully!'
    msg.html = render_template('emailtemplates/getinvited.html', email = email)
    mail.send(msg)
       
    flash("You got added to the waitinglist, keep an eye on your mailbox", category='success')
    return render_template("getinvited.html", user = 'none')



#This function triggers an email to the user if he signs up for Frankly
def newuserconfirmation(recipient):
   msg = Message(
                'Welcome to Frankly!',
                sender ='noreply@franklyapp.nl',
                recipients = [recipient]
               )
   msg.body = 'Welcome to Frankly! Your account was registered succesfully!'
   msg.html = render_template('emailtemplates/welcome.html')
   mail.send(msg)

#This function triggers if the user resets their password
def newpasswordconfirmation(recipient):
   msg = Message(
                'Your Frankly password was reset succesfully!',
                sender ='noreply@franklyapp.nl',
                recipients = [recipient]
               )
   msg.body = 'Your Frankly password was reset succesfully!'
   msg.html = render_template('emailtemplates/passwordresetconfirm.html')
   mail.send(msg)

# This function sends the user a token to reset their password
def passwordresettoken(recipient, token):
   msg = Message(
                'Reset your Frankly password',
                sender ='noreply@franklyapp.nl',
                recipients = [recipient]
               )
   msg.body = 'Reset your Frankly password by clicking this link: https://franklyapp.nl/reset-password/'+token
   msg.html = render_template('emailtemplates/passwordreset.html', token = token)
   mail.send(msg)   


# This function sends the user a confirmation after paying
def invoiceconfirmation(userid):
  user = User.query.filter_by(id=userid).first()
  recipient = user.email
  invoicedate = datetime.today().strftime('%Y-%m-%d')
  msg = Message(
              'Your Frankly Invoice',
              sender ='noreply@franklyapp.nl',
              recipients = [recipient]
              )
  msg.html = render_template('emailtemplates/invoice.html', invoicedate= invoicedate, userid = userid, email = recipient, username = user.username, phonenumber = user.phonenumber)
  mail.send(msg)      
     

  


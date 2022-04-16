from curses import flash
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
from flask_login import login_required, current_user
from configparser import ConfigParser
from twilio.rest import Client 
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from . import db
from . import mail
from .models import Post, User, Comment, Like
from flask_mail import Mail, Message


messaging = Blueprint("messaging", __name__)

#fetching credentials used on this page
config = ConfigParser()
config.read('Env_Settings.cfg')
#Twilio ID
account_sid = config.get('account_sid', 'account_sid')
auth_token = config.get('auth_token', 'auth_token')
#bitly ID
bitlykey = config.get('bitlykey', 'bitlykey')
#Sendgrid ID
sendgrid_api = config.get('sendgrid_api', 'sendgrid_api')



#From here we have the Twillio Whatsapp integration
@messaging.route("/sendwhatsapp/<userid>/<phonenumber>")
@login_required
def SendWhatsapp(userid, phonenumber):
    user = User.query.filter_by(id=userid).first()
    client = Client(account_sid, auth_token) 
    phonenumber = str(phonenumber)
    promotorURL = str('\n\n\n😃 great! > https://grapevine.works/send-feedback/'+userid+'/3')
    neutralURL = str('\n\n\n😑 mehh! > https://grapevine.works/send-feedback/'+userid+'/2')
    detractorURL = str('\n\n\n😢 Not so good > https://grapevine.works/send-feedback/'+userid+'/1')
    message = user.customquestion0
    sender= user.userpublicname
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
    
    print(message.sid)
    flash("Message sent to your phone, check your Whatsapp!", category='success')
    return('', 204) 

#From here we have the email integration
@messaging.route("/sendemail/<userid>/<email>")
@login_required
def SendEmail(userid, email):
    user = User.query.filter_by(id=userid).first()
    email = str(email)
    promotorURL = str('https://grapevine.works/send-feedback/'+userid+'/3')
    neutralURL = str('https://grapevine.works/send-feedback/'+userid+'/2')
    detractorURL = str('https://grapevine.works/send-feedback/'+userid+'/1')
    sender= user.userpublicname
    message = Mail(
    from_email=user.userpublicname+'@grapevine.works',
    to_emails=email,
    subject= user.customquestion0,

    #THis next section is the HTML email body: NOTE IT"S NOT A COMENT
    html_content='''
     <html>
    <head>
      <title></title>
    </head>
    <body>
      <div data-role="module-unsubscribe" class="module" role="module" data-type="unsubscribe" style="color:#444444; font-size:12px; line-height:20px; padding:16px 16px 16px 16px; text-align:Center;" data-muid="4e838cf3-9892-4a6d-94d6-170e474d21e5">
      
      
      <h1>'''+user.customquestion0+'''</H1>
      <p>'''+user.customquestion0+''', click the emoji that best suits your experience:</p>
      <h1>
            <a href="'''+promotorURL+'''" target="_blank" style="font-family:sans-serif;text-decoration:none;">
            😃 great!</a>
            <a href="'''+neutralURL+'''" target="_blank" style="font-family:sans-serif;text-decoration:none;">
            😑 mehh!</a>
              <a href="'''+detractorURL+'''" target="_blank" style="font-family:sans-serif;text-decoration:none;">
            😢 Not so good</a>
        </h1>    
        <p style="font-size:12px; line-height:20px;">
          <a class="Unsubscribe--unsubscribeLink" href="{{{unsubscribe}}}" target="_blank" style="font-family:sans-serif;text-decoration:none;">
            Unsubscribe
          </a>
          -
          <a href="{{{unsubscribe_preferences}}}" target="_blank" class="Unsubscribe--unsubscribePreferences" style="font-family:sans-serif;text-decoration:none;">
            Unsubscribe Preferences
          </a>
        </p>
      </div>
    </body>
  </html>
    
    ''')
    try:
        sg = SendGridAPIClient(sendgrid_api)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
    flash("Template sent to your mailbox, check your email!", category='success')
    return('', 204) 



#From here for the waiting list
@messaging.route("/getinvited", methods=['GET', 'POST'])
def getinvited():
  if request.method == 'GET':
    return render_template("getinvited.html", methods = ['GET', 'POST'])
  else:
    email = request.form.get("email")  
    email = str(email)
    print(email)
    message = Mail(
    from_email=('invites@grapevine.works', 'Grapevine'),
    subject='We added you to our waiting list ',
    html_content='<p>Keep an eye on your mailbox, as we will send you an invite to start using Grapevine soon!</p>',
    # for improved deliverability, provide plain text content in addition to html content
    to_emails=email)
    try:
        sg = SendGridAPIClient(sendgrid_api)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
       
    flash("You got added to the waitinglist, keep an eye on your mailbox", category='success')
    return render_template("getinvited.html")


#Here we send emails using our own emailserver (not Sendgrid)
@messaging.route("/testemail")
def index():
   msg = Message(
                'Hello',
                sender ='noreply@franklyapp.nl',
                recipients = ['peter@petervandoorn.com']
               )
   msg.body = 'Hello Flask message sent from Flask-Mail'
   mail.send(msg)
   return 'Sent'

#This function triggers an email to the user if he signs up for Frankly
def newuserconfirmation(recipient):
   msg = Message(
                'Welcome to Frankly!',
                sender ='noreply@franklyapp.nl',
                recipients = [recipient]
               )
   msg.body = 'Welcome to Frankly! Your account was registered succesfully!'
   mail.send(msg)

#This function triggers if the user resets their password
def newpasswordconfirmation(recipient):
   msg = Message(
                'Your Frankly password was reset succesfully!',
                sender ='noreply@franklyapp.nl',
                recipients = [recipient]
               )
   msg.body = 'Your Frankly password was reset succesfully!'
   mail.send(msg)

# This function sends the user a token to reset their password
def passwordresettoken(recipient, token):
   msg = Message(
                'Reset your Frankly password',
                sender ='noreply@franklyapp.nl',
                recipients = [recipient]
               )
   msg.body = 'Reset your Frankly password by clicking this link: https://grapevine.works/reset-password/'+token
   mail.send(msg)   
     

  


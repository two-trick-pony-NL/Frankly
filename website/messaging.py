from curses import flash
import pyshorteners
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
from flask_login import login_required, current_user
from configparser import ConfigParser
from twilio.rest import Client 
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

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
    client = Client(account_sid, auth_token) 
    phonenumber = str(phonenumber)
    promotorURL = str('\n\n\n😃 great! > https://grapevine.works/send-feedback/'+userid+'/3')
    neutralURL = str('\n\n\n😑 mehh! > https://grapevine.works/send-feedback/'+userid+'/2')
    detractorURL = str('\n\n\n😢 Not so good > https://grapevine.works/send-feedback/'+userid+'/1')
    message = 'Thanks, what did you think of the workshop?'
    print(userid)
    

    message = client.messages.create( 
                                messaging_service_sid='MGcda453ae1d2d1f05cb4b8124367535b5', 
                                #To enable whatsapp add this line in again
                                #from_='whatsapp:+14155238886',  
                                body=message+promotorURL+neutralURL+detractorURL,      
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
    email = str(email)
    promotorURL = str('https://grapevine.works/send-feedback/'+userid+'/3')
    neutralURL = str('https://grapevine.works/send-feedback/'+userid+'/2')
    detractorURL = str('https://grapevine.works/send-feedback/'+userid+'/1')
    message = Mail(
    from_email='no-reply@grapevine.works',
    to_emails=email,
    subject='Your Grapevine email template',
    html_content='''
     <html>
    <head>
      <title></title>
    </head>
    <body>
      <div data-role="module-unsubscribe" class="module" role="module" data-type="unsubscribe" style="color:#444444; font-size:12px; line-height:20px; padding:16px 16px 16px 16px; text-align:Center;" data-muid="4e838cf3-9892-4a6d-94d6-170e474d21e5">
      
      
      <h1>How did you like our workshop?</H1>
      <p>Tell us how you liked the workshop last friday, click the emoji that best suits your experience:</p>
            <a href="'''+promotorURL+'''" target="_blank" style="font-family:sans-serif;text-decoration:none;">
            😃 great!</a>
            <a href="'''+neutralURL+'''" target="_blank" style="font-family:sans-serif;text-decoration:none;">
            😑 mehh!</a>
              <a href="'''+detractorURL+'''" target="_blank" style="font-family:sans-serif;text-decoration:none;">
            😢 Not so good</a>
            
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
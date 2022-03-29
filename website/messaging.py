from curses import flash
import pyshorteners
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
from flask_login import login_required, current_user
from configparser import ConfigParser
from twilio.rest import Client 
import smtplib, ssl

messaging = Blueprint("messaging", __name__)


config = ConfigParser()
config.read('Env_Settings.cfg')
account_sid = config.get('account_sid', 'account_sid')
auth_token = config.get('auth_token', 'auth_token')
bitlykey = config.get('bitlykey', 'bitlykey')

"""
long_url = input("Enter the URL to shorten: ")

#TinyURL shortener service
type_bitly = pyshorteners.Shortener(api_key=bitlykey)
short_url = type_bitly.bitly.short(long_url)
 
print("The Shortened URL is: " + short_url)
"""

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
                                from_='whatsapp:+14155238886',  
                                body=message+promotorURL+neutralURL+detractorURL,      
                                to='whatsapp:'+phonenumber
                            ) 
    
    print(message.sid)
    flash("Message sent to your phone, check your Whatsapp!", category='success')
    return('', 204) 

#From here we have the email integration
@messaging.route("/sendemail/<userid>/<email>")
@login_required
def SendEmail(userid, email):
    email = str(email)
    promotorURL = str('\n\n\n😃 great! > https://grapevine.works/send-feedback/'+userid+'/3')
    neutralURL = str('\n\n\n😑 mehh! > https://grapevine.works/send-feedback/'+userid+'/2')
    detractorURL = str('\n\n\n😢 Not so good > https://grapevine.works/send-feedback/'+userid+'/1')
    message = 'Thanks, what did you think of the workshop?'
    smtp_server = "mail.petervandoorn.com"
    port = 587  # For starttls
    sender_email = "grapevine@petervandoorn.com"
    receiver_email = email
    password = "GrapeVineMetJoep"
    context = ssl.create_default_context()

    message = """\
                Subject: Hi there

                This message is sent from Python."""


    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        # Create a secure SSL context
        

        # Try to log in to server and send email
        try:
            server = smtplib.SMTP(smtp_server,port)
            server.ehlo() # Can be omitted
            server.starttls(context=context) # Secure the connection
            server.ehlo() # Can be omitted
            server.login(sender_email, password)
            # TODO: Send email here
        except Exception as e:
            # Print any error messages to stdout
            print(e)
        finally:
            server.quit() 

        return('', 204) 
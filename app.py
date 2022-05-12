from sqlalchemy import true
from website import create_app
from configparser import ConfigParser

#By calling the create app function the app is initialised from the __init.py file
app = create_app
print("Creating the app")
#This line is disabled so that Gunicorn can take port 80 to expose to the public. 
#app.run(debug=True, host='0.0.0.0', port=80)
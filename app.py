from sqlalchemy import true
from website import create_app

app = create_app()
#This line is disabled so that Gunicorn can take port 80 to expose to the public. 
#app.run(debug=True, host='0.0.0.0', port=80)
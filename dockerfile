# Set base image (host OS)
FROM python:3.12-rc-slim-bullseye

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /Franklyapp

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip3 install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY app.py .
COPY gunicorn.sh .
COPY website ./website
COPY Env_Settings.cfg .
# Specify the command to run on container start
#CMD [ "python3", "./app.py" ]
ENTRYPOINT ["./gunicorn.sh"]

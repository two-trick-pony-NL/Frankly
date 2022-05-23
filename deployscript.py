import os
import time
epoch_time = int(time.time())
print(epoch_time)


#This file helps deploy the application by building the dockerfile and sending the docker image to amazon


print("\n########################\n")
print("\n---Deployment started---\n")
print("\n########################\n")
print("\n########################\n")
os.system("echo Creating Container image")
print("\n########################\n")

#The slashes are used to ignore the " character

os.system("docker build --pull --rm -f \"dockerfile\" -t franklyapp:latest \".\"")

print("\n########################\n")
print("\n\nContainer created!\n\n")
print("\n########################\n")

print("\n########################\n")
print("\n\n pushing container to Amazon Web Services Lightsail\n\n")
print("\n########################\n")
os.system("aws lightsail push-container-image --region eu-central-1 --service-name franklyapp --label franklyapp --image franklyapp:latest")

print("\n########################\n")
print("\n\nImage pushed to Lightsail\n\n")
print("\n########################\n")

print("\n########################\n")
print("\nImage is deployed on AWS Lightsail. It might take a few minutes to appear online\nLog in here to verify it's status: https://lightsail.aws.amazon.com/ls/webapp/home/instances\n")
print("\n########################\n")
print("Here is the configuration file: ")
os.system("aws lightsail create-container-service-deployment --service-name franklyapp \
--containers file://AWS/deploymentconfig.json \
--public-endpoint file://AWS/publicendpoint.json")
print("\n########################\n")
print("Here are the logs of the last 24H")
print("\n########################\n")
#Getting the logs of the container with the preferences set so as in the file. The epoch at 3600 specifies all logs of the last hour

os.system("aws lightsail get-container-log --cli-input-json file://AWS/scriptpreferences.json --start-time " +str(epoch_time-86400))   

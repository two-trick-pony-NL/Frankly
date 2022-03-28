import os


#This file helps deploy the application by building the dockerfile and sending the docker image to amazon


print("\n########################\n")
print("\n---Deployment started---\n")
print("\n########################\n")
print("\n########################\n")
os.system("echo Creating Container image")
print("\n########################\n")

#The slashes are used to ignore the " character

os.system("docker build --pull --rm -f \"dockerfile\" -t grapevine:latest \".\"")

print("\n########################\n")
print("\n\nContainer created!\n\n")
print("\n########################\n")

print("\n########################\n")
print("\n\n pushing container to Amazon Web Services Lightsail\n\n")
print("\n########################\n")
os.system("aws lightsail push-container-image --region eu-central-1 --service-name grapevine --label grapevine --image grapevine:latest")

print("\n########################\n")
print("\n\nImage pushed to Lightsail\n\n")
print("\n########################\n")

print("\n########################\n")
print("\n\Image is deployed on AWS Lightsail. It might take a few minutes to appear online\nLog in here to verify it's status: https://lightsail.aws.amazon.com/ls/webapp/home/instances\n")
print("\n########################\n")
print("Here is the configuration file: ")
os.system("aws lightsail create-container-service-deployment --service-name grapevine \
--containers file://AWS/deploymentconfig.json \
--public-endpoint file://AWS/publicendpoint.json")

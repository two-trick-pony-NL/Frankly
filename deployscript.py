import os
print("#####################")
print(" \nDeployment started \n")
print("#####################")

os.system("echo Creating Container image")

#The slashes are used to ignore the " character
os.system("docker build --pull --rm -f \"dockerfile\" -t grapevine:latest \".\"")

print("\n\nContainer created!\n\n")
print("\n\n pushing container to Amazon Web Services Lightsail")
os.system("aws lightsail push-container-image --region eu-central-1 --service-name grapevine --label grapevine --image grapevine:latest")
print("\n\nImage pushed to Lightsail\n\n")
print("\n\nDeploying image on AWS Lightsail\n\n")
os.system("aws lightsail create-container-service-deployment --service-name grapevine \
--containers file://deploymentconfig.json \
--public-endpoint file://publicendpoint.json")

print("\n\n Deployment completed!")

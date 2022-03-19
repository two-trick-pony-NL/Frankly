import os
print("#####################")
print(" \nDeployment started \n")
print("#####################")

os.system("echo Creating Container image")

#The slashes are used to ignore the " character
os.system("docker build --pull --rm -f \"dockerfile\" -t grapevine:latest \".\"")

print("Container created!\n\n")

print("echo pushing container to Lightsail")
os.system("aws lightsail create-container-service-deployment --service-name grapevine \
--containers file://deploymentconfig.json \
--public-endpoint file://publicendpoint.json")

print("\n\n Deployment completed!")

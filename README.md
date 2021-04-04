#Part 1  - deploy flask app on AWS using lightsail
https://aws.amazon.com/getting-started/hands-on/serve-a-flask-app/

#Prerequisites
Docker - https://docs.docker.com/engine/install/
AWS CLI - https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-windows.html#cliv2-windows-install
Lightsail Control - https://lightsail.aws.amazon.com/ls/docs/en_us/articles/amazon-lightsail-install-software

#Build docker container

docker build -t raz-flask-container .

#Create aws lightsail service

aws lightsail create-container-service --service-name flask-service --power small --scale 1

aws lightsail get-container-services --service-name flask-service

#Push container image to lightsail

aws lightsail push-container-image --service-name flask-service --label raz-flask-container --image raz-flask-container

#Deploy the container
aws lightsail create-container-service-deployment --service-name flask-service --containers file://containers.json --public-endpoint file://public-endpoint.json

aws lightsail get-container-services --service-name flask-service


#Cleanup
aws lightsail delete-container-service --service-name flask-service


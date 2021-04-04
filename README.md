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

Part 2
https://thecodinginterface.com/blog/aws-sam-serverless-rest-api-with-flask/

https://medium.com/swlh/deploying-a-python-flask-application-to-aws-lambda-with-serverless-framework-and-circleci-3f57437f0758

Prerequisits
#https://www.serverless.com/ - platfrom agnostic (AWS SAM Severless Application Model is AWS only)
npm install -g serverless

#plugins required for your Flask application in the context of Serverless Framework
npm install serverless-wsgi serverless-python-requirements --save-dev

#AWS Serverless Application Model CLI
https://github.com/awslabs/aws-sam-cli/releases/latest/download/AWS_SAM_CLI_64_PY3.msi



sam build --region eu-central-1

sam deploy --stack-name flask-aws --guided 

aws cloudformation delete-stack --stack-name flask-aws



http -j POST https://warw1v5s2e.execute-api.eu-central-1.amazonaws.com/Prod/lists "Authorization:bearer 12345" name=Groceries items:='[{"name":"milk", "completed":false},{"name":"cookies", "completed":false}]'
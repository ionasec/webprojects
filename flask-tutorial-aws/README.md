https://flask.palletsprojects.com/en/1.1.x/tutorial/layout/

> $env:FLASK_APP = "flaskr"
> $env:FLASK_ENV = "development"
> flask run

https://flask.palletsprojects.com/en/1.1.x/tutorial/tests/


pip install -e .

pytest

coverage run -m pytest

https://flask.palletsprojects.com/en/1.1.x/tutorial/deploy/

pip install wheel

python setup.py bdist_wheel

$ export FLASK_APP=flaskr
$ flask init-db

in production

pip install waitress
waitress-serve --call 'flaskr:create_app'

Serving on http://0.0.0.0:8080


--
BUILD 
docker build -t raz-flask-tutorial .  

RUN
docker run -p 8080:8080 raz-flask-tutorial

CREATE AWS LIGHTSAIL FALSK SERVICE
aws lightsail create-container-service --service-name flask-service --power small --scale 1

PUSH container image to lightsail

aws lightsail push-container-image --service-name flask-service --label raz-flask-tutorial --image raz-flask-tutorial

DEPLOY
aws lightsail create-container-service-deployment --service-name flask-service --containers file://containers.json --public-endpoint file://public-endpoint.json

CHECK
aws lightsail get-container-services --service-name flask-service
#Cleanup
aws lightsail delete-container-service --service-name flask-service

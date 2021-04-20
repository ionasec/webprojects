from config import config
from flask import Flask, render_template_string, session, redirect, request, url_for, g
from lambda_wrapper import FlaskLambda
import os
import uuid
import boto3
import flask_login
import requests
from datetime import datetime
#from flask_serverless import Serverless, Flask, APIGWProxy
#import aws_lambda_wsgi


def create_app(config_name='default'):
   
    #app = Flask(__name__)
    #lambda_handler =  lambda event, context: aws_lambda_wsgi.response(app, event, context)

 
    app = FlaskLambda(__name__)
    #app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.secret_key = app.config['FLASK_SECRET']


  #  os.environ['SCRIPT_NAME'] = "/"+os.environ['EXECENV']
  #  print(os.environ['SCRIPT_NAME'])
    print("app.root_path:"+app.root_path)

    from . import home
    app.register_blueprint(home.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    
    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)
    @login_manager.user_loader
    def user_loader(session_token):
        if "expires" not in session:
                return None

        expires = datetime.utcfromtimestamp(session['expires'])
        expires_seconds = (expires - datetime.utcnow()).total_seconds()
        if expires_seconds < 0:
            return None

        user = auth.User()
        user.id = session_token
        user.nickname = session['nickname']
        g.user = user.nickname
        return user




    return app



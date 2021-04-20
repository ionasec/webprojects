import os
from app import util

#PREFIX = "/"+os.environ['EXECENV']


class Config:
    @staticmethod
    def init_app(app):
        pass

    AWS_REGION = os.environ['AWSREGION']

    AWS_COGNITO_POOL_ID = os.environ['AWSCOGNITOPOOLID']
    AWS_COGNITO_CLIENT_ID = os.environ['AWSCOGNITOCLIENTID']
    AWS_COGNITO_CLIENT_SECRET = os.environ['AWSCOGNITOCLIENTSECRET']
    AWS_COGNITO_DOMAIN = os.environ['AWSCOGNITODOMAIN']
    BASE_URL = os.environ['BASEURL']

    AWS_DYNAMODB_TABLE_NAME = os.environ['AWSDYNAMODBTABLENAME']
    AWS_S3_BUCKET = os.environ['AWSS3BUCKET']

    FLASK_SECRET = util.random_hex_bytes(8)
#https://dlukes.github.io/flask-wsgi-url-prefix.html
    EXECENV = os.environ['EXECENV']
    #SERVER_NAME = "/prod"

class LocalDevelopmentConfig(Config):
    DEBUG = True
    AWS_DYNAMODB_LOCAL_URL ="http://localhost:8000"

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    DEBUG = True
    PROD = True


config = {
    'local' : LocalDevelopmentConfig,
    'dev': DevelopmentConfig,
    'testing': TestingConfig,
    'prod': ProductionConfig,
    'default': ProductionConfig
}
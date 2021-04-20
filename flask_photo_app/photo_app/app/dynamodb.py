from flask import current_app, g
from boto3.dynamodb.conditions import Key

import boto3

def db_table(table_name='default'):
    if table_name == 'default':
        table_name=current_app.config['AWS_DYNAMODB_TABLE_NAME']
    return get_db().Table(table_name)


def close_db(e=None):
    db = g.pop('db', None)

def get_db():
    if 'db' not in g:
        if  current_app.config['EXECENV'] == 'local':
            g.db = boto3.resource('dynamodb', endpoint_url=current_app.config['AWS_DYNAMODB_LOCAL_URL'])
        else:
            g.db = boto3.resource('dynamodb', region_name=current_app.config['AWS_REGION'])
    print(g.db)
    return g.db


def add_photo_textonly(title, body, cognito_username,timestamp):
    print("!!!add phott")
    print(title, body, cognito_username)
    response = db_table().put_item(
        Item={
            'username' : cognito_username,
            'title': title,
            'body': body,
            'timestamp' : timestamp
        }
    )
    print(response)
    return response

def add_photo(title, body, image_file, cognito_username,timestamp):
    print("!!!add phott")
    print(title, body, image_file, cognito_username)
    response = db_table().put_item(
        Item={
            'username' : cognito_username,
            'title': title,
            'body': body,
            'image_file': image_file,
            'timestamp' : timestamp
        }
    )
    print(response)
    return response

def list_user_photos(cognito_username):
    print("!!!list_user_photos")
    response = db_table().query(
        KeyConditionExpression=Key('username').eq(cognito_username)
    )
    return response['Items']

def list_all_photos(cognito_username):
    "Select all the photos from the database"
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""SELECT object_key, description, labels, created_datetime
        FROM photo WHERE cognito_username = %s
        ORDER BY created_datetime desc""", (cognito_username,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

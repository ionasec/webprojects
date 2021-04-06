import os

#os.environ['FLASK_APP'] = "flaskr"

try:
    os.makedirs('instance')
except OSError:
    pass

os.system('flask init-db')
#os.system('flask init-s3')
os.system('waitress-serve --call flaskr:create_app')

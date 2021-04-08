import os

os.environ['FLASK_APP'] = "flaskr"

os.system('flask init-db')
#os.system('flask init-s3')

#os.system('waitress-serve --listen=127.0.0.1:8080 --call flaskr:create_app')
#os.system('flask run -p 3002')
os.system('waitress-serve --call flaskr:create_app')

import os
os.system('flask init-db')
os.system('waitress-serve --call flaskr:create_app')

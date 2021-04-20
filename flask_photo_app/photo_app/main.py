import os
from app import create_app



app = create_app(os.getenv('EXECENV') or 'default')


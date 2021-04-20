# Python Virtual Envrirnoment 
https://pypi.org/project/pipenv/

# Create a new project using Python 3.7, specifically:
pipenv --python 3.8

# Spawns a shell within the virtualenv.
pipenv shell 

# Install Packages
pip install -r .\photo_app\requirements.txt

# Test local
flask run

# build cloud formation template
sam build

# deploy stack
sam deploy --stack-name raz-photo-appx --guided

# re run update yaml template with updated value for the below
sam deploy --stack-name raz-photo-appx --guided
# AWSCOGNITOPOOLID
# AWSCOGNITOCLIENTID
# AWSCOGNITOCLIENTSECRET
# AWSCOGNITODOMAIN - EXAMPLE "raztest.auth.eu-central-1.amazoncognito.com"
# BASEURL https://r2exwbfwjh.execute-api.eu-central-1.amazonaws.com/prod

# in Cognito console - enable idp for app client

#Python Virtual Envrirnoment 
https://pypi.org/project/pipenv/

#Create a new project using Python 3.7, specifically:
pipenv --python 3.8

#Spawns a shell within the virtualenv.
pipenv shell 

#Install Packages
pip install -r .\requirements.txt

#Build and deploy 
sam build
sam deploy --guided (run twice
)
Parameter AWSCOGNITOPOOLID [AWSCOGNITOPOOLID]: eu-central-1_jHopeOVIx
Parameter AWSCOGNITOCLIENTID [AWSCOGNITOCLIENTID]: od3amomvpdimd67e2n6c1qdm6
Parameter AWSCOGNITOCLIENTSECRET [AWSCOGNITOCLIENTSECRET]: 1j1uqqbv01f8h524qi1vm4pafd6tpiunvt80jfafmrmrnokr1t40
Parameter AWSCOGNITODOMAIN userpool-test-01.auth.eu-central-1.amazoncognito.com
Parameter BASEURL https://1saan8kf9j.execute-api.eu-central-1.amazonaws.com/prod

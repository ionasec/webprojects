# Set base image (host OS)
FROM python:3.8-alpine

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /app

# copy the dependencies file to the working directory
COPY requirements.txt .
# copy the content of the local src directory to the working directory
COPY flaskr/ ./flaskr
# copy bootstrap py
COPY run.py .

# install dependencies
RUN pip install -r requirements.txt



ENV FLASK_APP=flaskr
#RUN flask init-db

# Specify the command to run on container start
#CMD ["ls"]
CMD [ "python", "run.py" ]
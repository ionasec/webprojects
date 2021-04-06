
import os
from flask import Flask, flash, request, redirect, url_for
from flask import current_app, g
from werkzeug.utils import secure_filename
import boto3, botocore

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


s3 = boto3.client(
    "s3",
    aws_access_key_id=current_app.config['AWS_ACCESS_KEY'],
    aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY']
)

def upload_file_to_s3(file, acl="public-read"):
    filename = secure_filename(file.filename)
    try:
        s3.upload_fileobj(
            file,
            os.getenv("AWS_BUCKET_NAME"),
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e
    

    # after upload file to s3 bucket, return filename of the uploaded file
    return file.filename
     
     r1r

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_image_folder():
    print(app.config['SECRET_KEY'])

    if 'image_folder' not in g:
        g.image_folder = current_app.config['IMAGE_FOLDER'],

    return g.image_folder
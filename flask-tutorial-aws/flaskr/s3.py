import boto3, botocore
from flask import current_app, g

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}



def get_s3():
    if 's3' not in g:
        g.s3 = boto3.client(
        "s3",
        aws_access_key_id=current_app.config["S3_KEY"],
        aws_secret_access_key=current_app.config["S3_SECRET"],
        region_name ='eu-central-1'
        )
    return g.s3

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file_to_s3(file, bucket_name, acl="public-read"):

    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """
    print(file.filename)
    print(bucket_name)

    try:
        s3 = get_s3()
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename
        )
    except Exception as e:
        print("Something Happened: ", e)
        return e

    return "{}{}".format(current_app.config["S3_LOCATION"], file.filename)



def create_presigned_post(resource, bucket_name, expiration=100):
    try:
        s3 = get_s3()
        response = s3.generate_presigned_url('get_object', Params = {'Bucket': bucket_name, 'Key': resource}, ExpiresIn = 100)
    except Exception as e:
        return None

    return response
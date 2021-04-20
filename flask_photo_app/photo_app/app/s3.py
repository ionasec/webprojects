from flask import current_app, g

import boto3


def close_s3(e=None):
    s3 = g.pop('s3', None)

def get_s3():
    if 's3' not in g:
        if  current_app.config['EXECENV'] == 'local':
            g.s3 = boto3.resource('s3', endpoint_url=current_app.config['AWS_S3_LOCAL_URL'])
        else:
            g.s3 = boto3.resource('s3', region_name=current_app.config['AWS_REGION'])
    print(g.s3)
    return g.s3

def create_bucket(bucket_prefix='default'):
    if bucket_prefix == 'default':
        bucket_prefix=current_app.config['AWS_S3_BUCKET']

    session = boto3.session.Session()
    current_region = session.region_name
    bucket_name = create_bucket_name(bucket_prefix)
    bucket_response = get_s3().create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
        'LocationConstraint': current_region})
    print(bucket_name, current_region)
    return bucket_name, bucket_response

def upload_file_to_s3(file, bucket_name, acl="public-read"):

    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """
    print("filename:" + file.filename)
    print(bucket_name)
    session = boto3.session.Session()

    try:
        s3 = get_s3()
        s3.meta.client.upload_fileobj(
            file,
            bucket_name,
            file.filename
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e

    return "{}{}".format(current_app.config["AWS_S3_BUCKET"], file.filename)



def create_presigned_post(resource, bucket_name, expiration=100):
    print(bucket_name)
    print(resource)
    try:
        s3 = get_s3()
        response = s3.meta.client.generate_presigned_url('get_object', Params = {'Bucket': bucket_name, 'Key': resource}, ExpiresIn = 100)
        print("presigned:" + response)
    except Exception as e:
        return None

    return response
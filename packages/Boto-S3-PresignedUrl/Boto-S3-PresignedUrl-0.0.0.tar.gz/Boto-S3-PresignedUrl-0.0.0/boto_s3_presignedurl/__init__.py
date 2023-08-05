import boto3
import os

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID', None),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY', None)
)

def s3_presigned_url(bucket_name, file_name, expired_in=300):
    try:
        url = s3_client.generate_presigned_url('get_object',
                                               Params={'Bucket': bucket_name,
                                                       'Key': file_name},
                                               ExpiresIn=expired_in)
    except:
        print(f'Error: Amazon S3 Resource {bucket_name} {file_name} Not Found!')
        return None
    return url

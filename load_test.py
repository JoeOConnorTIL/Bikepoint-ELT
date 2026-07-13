import os
from dotenv import load_dotenv
import boto3

load_dotenv()
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

s3_client = boto3.client(
    's3',
    aws_access_key_id = AWS_ACCESS_KEY,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY
)

data = 'data/2026-07-08 16-17-26.json'
filename = '2026-07-08 16-17-26.json'

s3_client.upload_file(data, AWS_BUCKET_NAME, filename)
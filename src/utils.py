import boto3
from dotenv import load_dotenv
import os

load_dotenv()

session = boto3.Session(profile_name='demo-file-processor')
s3 = session.client('s3')
bucket_name = os.getenv('S3_BUCKET')


async def upload_file_to_s3(file, object_name):
    try:
        s3.upload_fileobj(file.file, bucket_name, object_name)
        return True
    except Exception as e:
        print(f"Error uploading file: {e}")
        return False
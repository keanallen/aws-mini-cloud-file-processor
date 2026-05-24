import json
import uuid

import boto3
from dotenv import load_dotenv
import os


load_dotenv()

def get_aws_session():
    profile = os.getenv('AWS_PROJECT_PROFILE')
    region = os.getenv('AWS_REGION')
    return boto3.Session(profile_name=profile, region_name=region)

def get_s3_client():
    session = get_aws_session()
    return session.client('s3')

def get_sqs_client():
    session = get_aws_session()
    return session.client('sqs')


async def upload_file_to_s3(file, object_name):
    try:
        s3 = get_s3_client()
        sqs = get_sqs_client()
        bucket_name = os.getenv('S3_BUCKET')
        s3.upload_fileobj(file.file, bucket_name, object_name)
        # notify sqs
        queue_url = os.getenv('SQS_QUEUE_URL')
        message = {
            "job_id": str(uuid.uuid4()),
            "bucket": bucket_name,
            "s3_key": object_name,
            "operation": "thumbnail"
        }

        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message)
        )
        return True
    except Exception as e:
        print(f"Error uploading file: {e}")
        return False
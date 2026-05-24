import json
import uuid

import boto3
from dotenv import load_dotenv
import os

load_dotenv()

session = boto3.Session(profile_name='demo-file-processor')
s3 = session.client('s3', region_name='us-east-1')
sqs = session.client('sqs', region_name='us-east-1')
bucket_name = os.getenv('S3_BUCKET')


async def upload_file_to_s3(file, object_name):
    try:
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
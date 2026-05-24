import json
import time
import os

from dotenv import load_dotenv
from PIL import Image
from src.utils import aws


load_dotenv()


def listen_sqs():
    sqs = aws.get_sqs_client()
    s3 = aws.get_s3_client()
    queue_url = os.getenv('SQS_QUEUE_URL')
    while True:
        try:
            print('Listening to SQS queue...')
            response = sqs.receive_message(
                QueueUrl=queue_url,
                AttributeNames=['All'],
                MaxNumberOfMessages=1,
                WaitTimeSeconds=20
            )

            messages = response.get('Messages', [])
            if not messages:
                continue

            message = messages[0]
            body = json.loads(message['Body'])

            bucket = body['bucket']
            key = body['s3_key']
            print("Received message: bucket=%s, key=%s" % (bucket, key))
            # download the file
            s3.download_file(bucket, key, '/tmp/' + key)
            # process the image
            img = Image.open('/tmp/' + key)
            img.thumbnail((300, 300))
            img.save('/tmp/thumbnail_' + key)
            # upload the thumbnail back to S3
            s3.upload_file('/tmp/thumbnail_' + key, bucket, 'thumbnails/thumbnail_' + key)
            # delete the message from the queue
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=message['ReceiptHandle']
            )
            print('Processed message successfully: bucket=%s, key=%s' % (bucket, key))
        except Exception as e:
            print('An error occurred while reading from sqs: %s' % str(e)) 
            time.sleep(10)
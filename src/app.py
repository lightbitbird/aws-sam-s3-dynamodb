import datetime
import json
import os
import urllib
from decimal import Decimal

import boto3
import time

rekognition_client = boto3.client('rekognition')
s3_client = boto3.client('s3')
dynamo_client = boto3.client('dynamodb')

# Get the table name from lambda environment
table_name = os.environ['TABLE_NAME']


def lambda_handler(event, context):
    # Get the object from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

    try:
        # Call rekognition DetectText API to detect labels in S3 object
        response = detect_text(bucket, key)
        textDetections = [text['DetectedText'] for text in response['TextDetections']]

        # Call rekognition DetectLabels API to detect labels in S3 object
        response = detect_labels(bucket, key)
        labels = [{label_prediction['Name']: Decimal(str(label_prediction['Confidence']))} for label_prediction in
                  response['Labels']]

        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        # Write to DynamoDB
        table = boto3.resource('dynamodb').Table(table_name)
        item = {'id': key, 'Datetime': timestamp, 'Labels': labels, 'Text': textDetections}
        table.put_item(Item=item)

        return 'Success'
    except Exception as e:
        print("Error processing object {} from bucket {}. Event {}".format(key, bucket, json.dumps(event, indent=2)))

        raise e


def detect_text(bucket, key):
    response = rekognition_client.detect_text(Image={"S3Object": {"Bucket": bucket, "Name": key}})
    return response


def detect_labels(bucket, key):
    response = rekognition_client.detect_labels(Image={"S3Object": {"Bucket": bucket, "Name": key}})
    return response

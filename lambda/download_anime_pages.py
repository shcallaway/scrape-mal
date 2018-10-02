import boto3
import urllib.request
import os
import json

BUCKET_NAME = os.environ["BUCKET_NAME"]


def request(url):
    print(f"GET {url}")

    try:
        return urllib.request.urlopen(url).read()
    except urllib.error.HTTPError as error:
        print(f"HTTPError: {error}")
        return None


def upload(bucket, key, body):
    client = boto3.client("s3")

    try:
        client.put_object(
            Bucket=bucket,
            Key=key,
            Body=body
        )
    except Exception as error:
        print(f"Error: {error}")


def handler(event, context):
    print(f"Event: {event}")

    id = ''

    try:
        id = json.loads(event["body"])["pageId"]
    except Exception as error:
        print(f"Error: {error}")
        return {
            "statusCode": 400
        }

    url = f"https://myanimelist.net/anime/{id}"
    key = f"anime/{id}.html"

    data = request(url)

    if data:
        upload(BUCKET_NAME, key, data)

        return {
            "statusCode": 201
        }

    return {
        "statusCode": 200
    }

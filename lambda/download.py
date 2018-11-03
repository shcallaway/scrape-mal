import boto3
import urllib.request
import os
import json

bucket = os.environ["BUCKET_NAME"]


def request(url):
    print(f"GET {url}")

    try:
        return urllib.request.urlopen(url).read()
    except urllib.error.HTTPError as error:
        print(f"HTTPError: {error}")
        return None


def respond_with(status_code):
    return {
        "statusCode": status_code
    }


def lambda_handler(event, context):
    print(f"Event: {event}")

    id = ''

    try:
        id = json.loads(event["body"])["mal_id"]
    except Exception as error:
        print(error)
        return respond_with(400)

    url = f"https://myanimelist.net/anime/{id}"
    key = f"anime/{id}.html"

    data = request(url)

    if data:
        client = boto3.client("s3")

        try:
            client.put_object(
                Bucket=bucket,
                Key=key,
                Body=data
            )
        except Exception as error:
            print(error)
            return respond_with(500)

        return respond_with(201)

    return respond_with(200)

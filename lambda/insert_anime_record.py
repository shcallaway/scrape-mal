# import boto3


def handler(event, context):
    print(f"Event: {event}")
    # This lambda should accept a JSON payload with data from
    # a scraped page and insert it into the database
    # client = boto3.client('rds')

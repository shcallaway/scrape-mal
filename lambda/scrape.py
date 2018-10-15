import json
import os
import botocore.vendored.requests as requests


def lambda_handler(event, context):
    mal_id = None

    try:
        mal_id = json.loads(event["body"])["mal_id"]
    except Exception as error:
        print(error)
        return {"statusCode": 400}

    url = os.environ["URL"]

    extract_api_key = os.environ["EXTRACT_API_KEY"]
    insert_api_key = os.environ["INSERT_API_KEY"]

    response = requests.post(
        f"{url}/default/extract",
        data=json.dumps({'mal_id': mal_id}),
        headers={'x-api-key': extract_api_key}
    )

    if response.status_code is not 200:
        return {"statusCode": 504}

    data = response.json()

    response = requests.post(
        f"{url}/default/insertAnimeRecord",
        data=json.dumps(data),
        headers={'x-api-key': insert_api_key}
    )

    return {"statusCode": 201}

import os
import bs4
import boto3
import json

fields = {
    'title': {
        'selector': '#contentWrapper > div:nth-of-type(1) > h1 > span',
        'index': 0
    },
    'alt_title_en': {
        'selector': '#content > table > tr > td.borderClass div.spaceit_pad',
        'index': 0
    },
    'alt_title_jp': {
        'selector': '#content > table > tr > td.borderClass div.spaceit_pad',
        'index': 1
    }
}


def get_html(mal_id):
    client = boto3.client("s3")

    try:
        bucket = os.environ["BUCKET_NAME"]
    except KeyError as error:
        print(f"Missing bucket name. Error: {error}")
        return None

    try:
        return client.get_object(
            Bucket=bucket,
            Key=f"anime/{mal_id}.html"
        )['Body'].read().decode()
    except Exception as error:
        print(f"Failed to get object from S3. Error: {error}")
        return None


def pretty_markup(string):
    return string.prettify().rstrip("\n\r")


def pretty_json(string):
    return json.dumps(string, indent=4, ensure_ascii=False)


def get_element_text(page, selector, index):
    element = get_element(page, selector, index)

    if element:
        # Remove any nodes that are elements; We only care about text
        contents = [node for node in element.contents if isinstance(node, str)]
        return "".join(contents).strip()

    return None


def get_element(page, selector, index):
    print(f"Selector: {selector}")
    print(f"Index: {index}")
    elements = page.select(selector)

    if len(elements) < 1:
        print("Selector didn't match anything.")
        return None

    try:
        element = elements[index]
    except IndexError:
        print(f"No element at index {index}.")
        return None

    print("Element:")
    print(pretty_markup(element))
    return element


def extract(mal_id):
    print(f"mal_id: {mal_id}")

    html = get_html(mal_id)
    html = bs4.BeautifulSoup(html, 'html.parser')

    data = {'mal_id': mal_id}

    for field, characteristics in fields.items():
        print(f"field: {field}")

        value = get_element_text(
            html, characteristics['selector'], characteristics['index'])

        print(f"value: {value}")

        if value:
            data[field] = value

    return data


def lambda_handler(event, context):
    mal_id = None

    try:
        mal_id = json.loads(event["body"])["mal_id"]
    except Exception as error:
        print(error)
        return {"statusCode": 400}

    data = None

    try:
        data = extract(mal_id)
    except Exception as error:
        print(error)
        return {"statusCode": 500}

    print(pretty_json(data))

    return {
        "statusCode": 200,
        "body": json.dumps(data, ensure_ascii=False)
    }

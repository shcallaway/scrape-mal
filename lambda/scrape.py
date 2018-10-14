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


def get_page(page_id):
    client = boto3.client("s3")

    try:
        bucket = os.environ["BUCKET_NAME"]
    except KeyError as error:
        print(f"Missing bucket name. Error: {error}")
        return None

    try:
        return client.get_object(
            Bucket=bucket,
            Key=f"anime/{page_id}.html"
        )['Body'].read().decode()
    except Exception as error:
        print(f"Failed to get object from S3. Error: {error}")
        return None


def pretty_markup(string):
    return string.prettify().rstrip("\n\r")


def pretty_json(string):
    return json.dumps(string, indent=4, ensure_ascii=False)


def get_text(element):
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


def scrape_page(id):
    print(f"Page: {id}")
    page = get_page(id)

    if not page:
        print("Skipping.")
        return

    page = bs4.BeautifulSoup(page, 'html.parser')

    data = {
        'page': id
    }

    for field, characteristics in fields.items():
        print(f"Field: {field}")

        element = get_element(
            page, characteristics['selector'], characteristics['index'])
        text = get_text(element)
        print(f"Text: {text}")

        if text:
            data[field] = text

    print(pretty_json(data))

    return data


def handler(event, context):
    print(f"Event: {event}")

    id = ''

    try:
        id = json.loads(event["body"])["pageId"]
    except Exception as error:
        print(error)
        return {
            "statusCode": 400
        }

    data = scrape_page(id)

    return {
        "statusCode": 200,
        "body": json.dumps(data, ensure_ascii=False)
    }

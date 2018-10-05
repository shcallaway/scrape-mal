import os
import bs4
import boto3

selectors = {
    'title': '#contentWrapper > div:nth-of-type(1) > h1 > span',
    'alt_title_en': '#content > table > tr > td.borderClass div.spaceit_pad',
    'alt_title_jp': '#content > table > tr > td.borderClass > div > div:nth-child(9)'
}


def get_page(page_id):
    try:
        aws_access_key_id = os.environ["AWS_ACCESS_KEY_ID"]
        aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
    except KeyError as error:
        print(f"Missing AWS credentials. Error: {error}")
        return None

    client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

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


def format_markup(markup):
    return markup.prettify().rstrip("\n\r")


def parent_selector(selector):
    # This only work with selectors that exclusively use direct parent symbols (>)
    print("Warning: This only works with selectors that exclusively use direct parent symbols (>)")
    selector = selector.split(" > ")[0:-1]
    return " > ".join(selector)


def get_text(element):
    if element:
        # Remove any nodes that are elements; We only care about text
        contents = [node for node in element.contents if isinstance(node, str)]
        return "".join(contents).strip()

    return None


def get_element(page, selector):
    print(f"Selecting: {selector}")
    elements = page.select(selector)

    if len(elements) > 1:
        raise Exception(f"The selector provided was not specific enough. It yielded multiple elements: {elements}")

    if len(elements) < 1:
        print("That didn't match anything.")
        # If the selector yielded nothing, try going up one level
        return get_element(page, parent_selector(selector))

    element = elements[0]
    print("Element:")
    print(format_markup(element))
    return element


def scrape_page(page_id):
    print(f"Page: {page_id}")
    # Download the html file for this page from S3
    page = get_page(page_id)

    if not page:
        print("Skipping.")
        return

    # Parse the html file into a traversable tree
    page = bs4.BeautifulSoup(page, 'html.parser')

    data = {}
    for field, selector in selectors.items():
        print(f"Field: {field}")

        element = get_element(page, selector)
        text = get_text(element)
        print(f"Text: {text}")

        if text:
            data[field] = text

    print(data)


scrape_page("103")

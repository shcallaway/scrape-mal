import os
import bs4
import boto3

selectors = {
  'title': '#contentWrapper > div:nth-of-type(1) > h1 > span',
  'alt_title_en': '#content > table > tbody > tr > td.borderClass > div > h2:nth-child(7)',
  'alt_title_jp': '#content > table > tbody > tr > td.borderClass > div > div:nth-child(9)'
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

def scrape_page(page_id):
  print(f"Page: {page_id}")

  def select(selector):
    elements = page.select(selector)

    try:
      print(f"Element: {elements[0]}")
      return elements[0]
    except IndexError:
      print("Could not find any elements!")
      print(f"Selector: {selector}")
      return None

  def get_contents(selector):
    element = select(selector)
    
    if element:
      return element.contents[0]

    return None
    
  page = get_page(page_id)

  if not page:
    print("Skipping.")
    return

  page = bs4.BeautifulSoup(page, 'html.parser')

  data = {}
  for field, selector in selectors.items():
    print(f"Field: {field}")
    contents = get_contents(selector)
    print(f"Contents: {contents}")

    if contents:
      data[field] = contents
  
  print(data)

scrape_page("5114")


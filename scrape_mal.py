import os
import bs4
import urllib.request

base_url = "https://myanimelist.net/anime/"

selectors = {
  'title': '#contentWrapper > div:nth-of-type(1) > h1 > span',
  'alt_title_en': '#content > table > tbody > tr > td.borderClass > div > h2:nth-child(7)',
  'alt_title_jp': '#content > table > tbody > tr > td.borderClass > div > div:nth-child(9)'
}

def get_filename(page_id):
  return f"pages/{page_id}"

def request_page(page_id):
  url = f"{base_url}/{page_id}"

  print(f"Visiting page at URL: {url}")

  try:
    return urllib.request.urlopen(url).read()
  except urllib.error.HTTPError as error:
    print(f"Encountered an HTTPError: {error}")
    return None

def read_page(page_id):
  filename = get_filename(page_id)

  print(f"Reading document from file: {filename}")
  f = open(filename, "rb")
  return f.read()

def get_page(page_id):
  if page_saved(page_id):
    return read_page(page_id)
  
  return request_page(page_id)

def page_saved(page_id):
  filename = get_filename(page_id)
  return os.path.exists(filename)

def scrape_page(page_id):
  def select(selector):
    elements = document.select(selector)
    print(f"Selected elements: {elements}")
    return elements[0]

  def get_contents(selector):
    return select(selector).contents[0]

  document = get_page(page_id)

  if not document:
    print("Skipping.")
    return

  document = bs4.BeautifulSoup(document, 'html.parser')

  data = {}
  for field, selector in selectors.items():
    print(f"Getting field: {field}")
    data[field] = get_contents(selector)
  
  print(data)

def save_page(page_id):
  document = request_page(page_id)

  filename = get_filename(page_id)
  print(f"Writing document to file: {filename}")  

  f = open(filename, "wb")
  f.write(document)

scrape_page("5114")
# scrape_page("5113")
# save_page("5114")


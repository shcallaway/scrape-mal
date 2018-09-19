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

  print(f"Reading page from file: {filename}")
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
    elements = page.select(selector)
    print(f"Selected elements: {elements}")
    return elements[0]

  def get_contents(selector):
    return select(selector).contents[0]

  page = get_page(page_id)

  if not page:
    print("Skipping.")
    return

  page = bs4.BeautifulSoup(page, 'html.parser')

  data = {}
  for field, selector in selectors.items():
    print(f"Getting field: {field}")
    data[field] = get_contents(selector)
  
  print(data)

def save_page(page_id):
  page = request_page(page_id)

  filename = get_filename(page_id)
  print(f"Writing page to file: {filename}")  

  f = open(filename, "wb")
  f.write(page)

scrape_page("5114")
# scrape_page("5113")
# save_page("5114")


import bs4
import urllib.request

base_url = "https://myanimelist.net/anime/"

selectors = {
  'title': '#contentWrapper > div:nth-of-type(1) > h1 > span'
}

def scrape_page(page_id):
  def select(selector):
    return document.select(selector)[0]

  def get_contents(selector):
    return select(selector).contents[0]

  url = f"{base_url}/{page_id}"
  
  print(f"Visiting page at URL: {url}")

  try:  
    document = urllib.request.urlopen(url).read()
  except urllib.error.HTTPError as error:
    print(f"Encountered an HTTPError: {error}")
    return  

  document = bs4.BeautifulSoup(document, 'html.parser')

  data = {}
  for field, selector in selectors.items():
    data[field] = get_contents(selector)
  
  print(data)

scrape_page("5114")
scrape_page("5113")

import csv
import os
import requests
from time import gmtime, strftime


# read datetime
current_time = strftime('%Y-%m-%d-%H-%M-%S', gmtime())
# create folder for batch based on datetime
current_directory = os.getcwd() # will want different directory
os.mkdir(current_time) # if not exists + error handling

# read list of websites to scrape
with open('news_sites.csv', newline='') as f:
    reader = csv.DictReader(f)
    rss_websites = [row for row in reader]

# for each website
for website in rss_websites:
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })
#   rotate proxy and header
    
#   get request to url
    request = requests.get(website['rss_url'], headers)
    xml = request.text
    
#   save text to .html file - name based on website id and/or datetime?
    with open(f"{current_time}/{website['id']}.xml", 'w') as f:
        f.write(xml)

# use config file for path to save scraped websites

# error handling?

# tests?
import pathlib
import requests
from utilities.data_struct import RotatingList
from utilities.files import csv_to_dict
from utilities.pathing import get_path_above
from time import gmtime, strftime
from typing import TypedDict


class Website(TypedDict):
    id: str
    name: str
    rss_url: str

user_agents = [
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 
    'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148', 
    'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36' 
]


def get_path_to_save() -> pathlib.Path: # should maybe take in root folder name to modularize, then rename
    """
    """
    app_root_path = get_path_above('in_the_news') # handle error or wrong path
    data_path = app_root_path.joinpath('data')
    # modularize time getting
    current_time = gmtime()
    year = strftime('%Y', current_time)
    month = strftime('%m', current_time)
    day = strftime('%d', current_time)
    hour = strftime('%H', current_time) #what if hour somehow overlaps? and something so no overwrite? pass hour in from airflow?
    return pathlib.Path(data_path, year, month, day, hour)


def scrape_websites(rss_websites: Website, parent_dir: pathlib.Path) -> None:
    """
    """
    parent_dir.mkdir(parents=True, exist_ok=True)
    headers_obj = RotatingList(user_agents) # rename
    
    for website in rss_websites:
        headers = headers_obj.next # rename
        
        # proxy + rotate proxy
        
        request = requests.get(website['rss_url'], headers) # thought i needed to add {user-agent: ...} ????
        xml = request.text
        
    #   check if html or xml for error/saving?
        with open(pathlib.Path(parent_dir, f"{website['id']}.xml"), 'w') as f:
            f.write(xml)

            
if __name__ == "__main__":
    csv_path = pathlib.Path(__file__).parent.joinpath('news_sites.csv')
    rss_websites = csv_to_dict(csv_path)

    path_to_save = get_path_to_save()

    scrape_websites(rss_websites, path_to_save)


# use config file for path to save scraped websites
# error handling?
# tests?
# async
# federalist returning forbidden ?
# rescrape with different header / proxy if scrape fails?
# docstrings
# utilities modules...
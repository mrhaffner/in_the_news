import json
import pathlib
import requests
from utilities.data_struct import RotatingList
from utilities.files import csv_to_dict
from utilities.pathing import get_path_with_current_datetime
from typing import TypedDict


class Website(TypedDict):
    id: str
    name: str
    rss_url: str


def scrape_websites_to_xml(rss_websites: Website, parent_dir: pathlib.Path) -> None:
    """
    Scrapes a list of rss_websites, saves each website to an xml file in parent_dir

    Throws IOError???
    """
    # move set up to another function or maybe created a scraped class to handle setup?
    json_path = pathlib.Path(__file__).parent.joinpath('config/user_agents.json')
    # needs error handling
    with open(json_path) as f:
        user_agents = json.load(f)

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
    csv_path = pathlib.Path(__file__).parent.joinpath('config/news_sites.csv')
    rss_websites = csv_to_dict(csv_path)

    path_to_save = get_path_with_current_datetime('in_the_news', 'data/scraped')

    scrape_websites_to_xml(rss_websites, path_to_save)


# use config file for path to save scraped websites
# error handling?
# tests?
# async
# federalist returning forbidden ?
# rescrape with different header / proxy if scrape fails?
# docstrings
# utilities modules...
# logs? maybe at airflow level?
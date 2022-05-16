import json
import random
import requests
from airflow.models import Variable
from pathlib import Path
from scripts.utilities.files import csv_to_dict
from scripts.utilities.pathing import add_datetime_to_path
from typing import TypedDict


class Website(TypedDict):
    id: str
    name: str
    rss_url: str


def _get_user_agent() -> str:
    """Returns a random user_agent string from configuration file."""
    json_path = Path(__file__).parent.joinpath('config/user_agents.json')
    with open(json_path) as f:
        user_agents = json.load(f)
    return user_agents[random.randint(0, len(user_agents) - 1)]


def _scrape_websites_to_xml(rss_websites: Website, parent_dir: Path) -> None:
    """Scrapes a list of rss_websites, saves each website to an xml file in parent_dir."""
    headers = {'User-agent': _get_user_agent()}
    parent_dir.mkdir(parents=True, exist_ok=True)
    
    for website in rss_websites:
        request = requests.get(website['rss_url'], headers = headers)
        xml = request.text
        with open(Path(parent_dir, f"{website['id']}.xml"), 'w') as f:
            f.write(xml)

            
def scraper() -> None:
    """Scrapes a list of websites from config csv file and saves them as xml files."""
    csv_path = Path(__file__).parent.joinpath('config/news_sites.csv')
    rss_websites = csv_to_dict(csv_path)

    # paths are created with base_dir and datetime passed in from airflow
    parsed_dir_root = Path(Variable.get('base_dir')).joinpath('data/scraped')
    path_to_save = add_datetime_to_path(parsed_dir_root, Variable.get('current_time'))

    _scrape_websites_to_xml(rss_websites, path_to_save)
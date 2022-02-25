import json
import pathlib
import requests
from utilities.data_struct import RotatingList
from utilities.files import csv_to_dict
from utilities.pathing import get_path_above
from utilities.pathing import add_datetime_to_path
from typing import TypedDict


class Website(TypedDict):
    id: str
    name: str
    rss_url: str


def get_path_to_save(base_dir_name: str, data_dir_name: str) -> pathlib.Path:
    """
        Finds the base path, adds a sub path, then adds a datetime based series of subpaths

        Example called path below @ 2022-02-22 02:22:22 with 'in_the_news' in path c/

        get_path_to_save('in_the_news', 'data')

        outputs Path:
        c/in_the_news/data/2022/02/22/02
    """
    #update docstring format?
    app_root_path = get_path_above(base_dir_name) # handle error or wrong path
    data_path = app_root_path.joinpath(data_dir_name)
    return add_datetime_to_path(data_path)


def scrape_websites(rss_websites: Website, parent_dir: pathlib.Path) -> None:
    """
    """
    json_path = pathlib.Path(__file__).parent.joinpath('config/user_agents.json')
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

    path_to_save = get_path_to_save('in_the_news', 'data')

    scrape_websites(rss_websites, path_to_save)


# use config file for path to save scraped websites
# error handling?
# tests?
# async
# federalist returning forbidden ?
# rescrape with different header / proxy if scrape fails?
# docstrings
# utilities modules...
# logs? maybe at airflow level?
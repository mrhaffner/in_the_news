import csv
import pathlib
import random
import requests
from time import gmtime, strftime
from typing import TypedDict


class Website(TypedDict):
    id: str
    name: str
    rss_url: str


def csv_to_dict(csv_file: pathlib.Path) ->list[Website]:
    """Converts a .csv file to an array of dictionaries"""

    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        output_dict = [row for row in reader]
    
    return output_dict


class Headers: # could use static instead of instance? better name? UserAgent? List Rotater with a list to input?
#doc string
    def __init__(self) -> None:
        self._headers_list = [ # read from file and instantiate?
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 
            'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148', 
            'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36' 
        ]
        self._headers_index = random.randint(0, len(self._headers_list) - 1)
        
    @property
    def headers(self) -> str:
        self._rotate_index()
        return self._headers_list[self._headers_index]

    def _rotate_index(self) -> None:
        self._headers_index += 1
        if self._headers_index == len(self._headers_list):
            self._headers_index = 0
    

def scrape_websites(rss_websites: Website, parent_dir: pathlib.Path) -> None:
    """
    """
    parent_dir.mkdir(parents=True, exist_ok=True)
    headers_obj = Headers()
    
    for website in rss_websites:
        headers = headers_obj.headers
        
        # proxy + rotate proxy
        
        request = requests.get(website['rss_url'], headers)
        xml = request.text
        
    #   check if html or xml for error/saving?
        with open(pathlib.Path(parent_dir, f"{website['id']}.xml"), 'w') as f:
            f.write(xml)


def is_current_folder_name(testcase: str, current_path: pathlib.Path) -> bool:
    """Returns true if the testcase is the same as the name of the current working folder"""
    return testcase == str(current_path)[-len(testcase):]


def get_path_above(folder_name: str) -> pathlib.Path or str: # should return one type
    """Finds path to folder above current path with specificed name"""
    current_directory = pathlib.Path(__file__).parent.absolute()

    while str(current_directory) != '/' or str(current_directory) != '\\':
        if is_current_folder_name(folder_name, current_directory):
            return current_directory

        current_directory = current_directory.parent.absolute()
    
    # throw error or return empty path?
    return ''


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
    hour = strftime('%H', current_time)
    return pathlib.Path(data_path, year, month, day, hour)

            
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
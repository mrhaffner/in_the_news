import csv
import pathlib
import random
import requests
from time import gmtime, strftime

# federalist returning forbidden ?

# read datetime
# current_time = strftime('%Y-%m-%d-%H-%M-%S', gmtime())
# create folder for batch based on datetime
# current_directory = os.getcwd() # will want different directory

# traverse directory tree until you reach in_the_news
# select data subfolder


# os.mkdir(current_time) # if not exists + error handling


def csv_to_dict(csv_file):
    """
        Converts a .csv file to an array of dictionaries
        input:
            csv_file: pathlib.Path
        output:
            [{}] ????
    """

    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        output_dict = [row for row in reader]
    
    return output_dict

class Headers:
    
    def __init__(self):
        self._headers_list = [
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 
            'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148', 
            'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36' 
        ]
        self._headers_index = random.randint(0, len(self._headers_list) - 1)
        self.headers = None
        self.set_new_headers()

    def set_new_headers(self):
        self.headers = requests.utils.default_headers()
        self.headers.update({'User-Agent': self._headers_list[self._headers_index]})

        self._headers_index += 1
        if self._headers_index == len(self._headers_list):
            self._headers_index = 0
    


def scrape_websites(rss_websites, parent_dir):
    parent_dir.mkdir(parents=True, exist_ok=True)
    header_obj = Headers()
    

    # for each website
    for website in rss_websites:
    #   rotate proxy and header - create class that automatically rotates
        headers = header_obj.headers
        header_obj.set_new_headers()
        
    #   get request to url
        request = requests.get(website['rss_url'], headers)
        xml = request.text
        
    #   save text to .html file - name based on website id and/or datetime?
    #   check if html or xml for error/saving?
        with open(pathlib.Path(parent_dir, f"{website['id']}.xml"), 'w') as f:
            f.write(xml)

# use config file for path to save scraped websites

# error handling?

# tests?

# async

# rescrape with different header / proxy if scrape fails?

def is_current_folder_name(testcase, current_path):
    """
        Returns true if the testcase is the same as the name of the current working folder
        paramaters:
            testcase: str
            current_path: pathlib.Path
        returns:
            bool
    """

    return testcase == str(current_path)[-len(testcase):]


def get_path_above(folder_name):
    """
        Finds path to folder above current path with specificed name
        parameters:
            folder_name: str
        output:
            pathlib.Path or str (make empty path or error?)
    """

    current_directory = pathlib.Path(__file__).parent.absolute()

    while str(current_directory) != '/' or str(current_directory) != '\\':
        if is_current_folder_name(folder_name, current_directory):
            return current_directory

        current_directory = current_directory.parent.absolute()
    
    # throw error or return empty path?
    return ''


def get_path_to_save():
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
import csv
import pathlib
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
    '''
    Converts a .csv file to a dictionary
    '''

    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        output_dict = [row for row in reader]
    
    return output_dict


def scrape_websites(rss_websites, parent_dir):
    parent_dir.mkdir(parents=True, exist_ok=True)

    # for each website
    for website in rss_websites:
        headers = requests.utils.default_headers()
        headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        })
    #   rotate proxy and header - create class that automatically rotates
        
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
    
    # throw error
    return ''
        
            
if __name__ == "__main__":
    csv_path = pathlib.Path(__file__).parent.joinpath('news_sites.csv')
    rss_websites = csv_to_dict(csv_path)

    # put this in its own method/class
    app_root_path = get_path_above('in_the_news') # handle error or wrong path
    data_path = app_root_path.joinpath('data')
    current_time = gmtime()
    year = strftime('%Y', current_time)
    month = strftime('%m', current_time)
    day = strftime('%d', current_time)
    hour = strftime('%H', current_time)
    path_to_save = pathlib.Path(data_path, year, month, day, hour)

    scrape_websites(rss_websites, path_to_save)
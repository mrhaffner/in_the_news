import csv
import os
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



def scrape_websites(rss_websites):
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
    #   check if html or xml for error/saving?
        with open(f"{current_time}/{website['id']}.xml", 'w') as f: # needs more sophisticated pathing
            f.write(xml)

# use config file for path to save scraped websites

# error handling?

# tests?


def is_current_folder_name(testcase, current_directory):
    '''
    Returns true if the testcase is the same as the name of the current working folder
    '''

    return testcase == str(current_directory)[-len(testcase):]


def get_data_path():
    current_directory = pathlib.Path(__file__).parent.absolute()

    if is_current_folder_name('in_the_news', current_directory):
        return current_directory
    else:
        while not is_current_folder_name('in_the_news', current_directory) or str(current_directory) == '/' or str(current_directory) == '\\':
            current_directory = current_directory.parent.absolute()
            print(current_directory)


if __name__ == "__main__":
    csv_path = pathlib.Path(__file__).parent.joinpath('news_sites.csv')
    rss_websites = csv_to_dict(csv_path)

    get_data_path()


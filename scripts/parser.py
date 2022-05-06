from ast import parse
import pathlib
from bs4 import BeautifulSoup

from utilities.article import article_factory

# takes in a datetime
# finds the appropriate folder at that datetime
# for each xml file in that folder, parses the xml rss file
# saves title, url, pubdate, and author? for each article in feed to db/or file? with specified datetime/website
# key can be url? or title+website?

# function that creates Article data class from 


# throws i/o error
def parse_soup(soup, publisher):
    items = soup.find_all('item')

    articles = []

    for item in items:
        # article = Article(item)
        article = article_factory(item, publisher)
        articles.append(article)

    return articles



# def save_xml_date(datetime)
    # convert datetime to path
    # loop over files in path
        # parse_xml(filepath)
        # save_to_whatver

#def soup_from_filepath(file_path):
    #with open(file_path) as fp:
        #soup = BeautifulSoup(fp, 'lxml')


if __name__ == "__main__":
    with open(pathlib.Path(__file__).parent.joinpath('tests/data/2022/05/03/18/breitbart.xml')) as f:
        npr_soup = BeautifulSoup(f, 'xml')

    parsed_soup = parse_soup(npr_soup, 'npr')
    for article in parsed_soup:
        print(article.__dict__)


    #print(parsed[0].__dict__)
   #save_xml_date(datetime?) 
   # date input from airflow?
    #with open(pathlib.Path(__file__).parent.joinpath('tests/data/2022/05/03/18/cnn.xml')) as f:
        #cnn_soup = BeautifulSoup(f, 'xml')
    #print(cnn_soup.find('item'))
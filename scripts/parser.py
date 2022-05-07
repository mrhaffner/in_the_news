import pandas as pd
import pathlib
from bs4 import BeautifulSoup
from utilities.article import article_factory
from utilities.pathing import get_path_with_current_datetime

# takes in a datetime
# finds the appropriate folder at that datetime
# for each xml file in that folder, parses the xml rss file
# saves title, url, pubdate, and author? for each article in feed to db/or file? with specified datetime/website
# key can be url? or title+website?

# function that creates Article data class from 

# throws i/o error
def save_parsed_articles(articles, publisher):
    # maybe get the path to save from based on input date folders from scraped folder
    dir_to_save = get_path_with_current_datetime('in_the_news', 'data/parsed')
    dir_to_save.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame([article for article in articles])
    df.to_parquet(pathlib.Path.joinpath(dir_to_save, publisher + '.parquet'))


# throws i/o error
def parse_articles_from_soup(soup, publisher):
    items = soup.find_all('item')

    articles = []

    for item in items:
        article = article_factory(item, publisher)
        articles.append(article)

    return articles


# throws i/o error
def parse_scraped_data(directory):
    for file in directory:
        if str(file).endswith('xml'):
            with open(file) as f:
                soup = BeautifulSoup(f, 'xml')
                articles = parse_articles_from_soup(soup, file.stem)
                save_parsed_articles(articles, file.stem)


if __name__ == "__main__":
    # this should find most recently scraped folder or generate a path based on datetime input
    dir_to_parse = pathlib.Path(__file__).parent.parent.joinpath('data/scraped/2022/05/07/17')
    parse_scraped_data(dir_to_parse.glob('*'))
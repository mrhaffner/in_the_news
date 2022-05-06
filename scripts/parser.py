import pathlib
from bs4 import BeautifulSoup

from utilities.article import article_factory

# takes in a datetime
# finds the appropriate folder at that datetime
# for each xml file in that folder, parses the xml rss file
# saves title, url, pubdate, and author? for each article in feed to db/or file? with specified datetime/website
# key can be url? or title+website?

# function that creates Article data class from 

def save_parsed_articles(articles):
    print(articles)

# throws i/o error
def parse_articles_from_soup(soup, publisher):
    items = soup.find_all('item')

    articles = []

    for item in items:
        article = article_factory(item, publisher)
        articles.append(article)

    return articles


def parse_scraped_data(directory):
    for file in directory:
        if str(file).endswith('xml'):
            with open(file) as f:
                soup = BeautifulSoup(f, 'xml')
                articles = parse_articles_from_soup(soup, file.stem)
                save_parsed_articles(articles)


if __name__ == "__main__":
    parse_scraped_data(pathlib.Path(__file__).parent.parent.joinpath('data/2022/05/06/21').glob('*'))
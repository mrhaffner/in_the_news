import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path
from typing import List
from utilities.article import Article, article_factory
from utilities.pathing import get_path_with_current_datetime


# throws i/o error
def save_parsed_articles(articles: List[Article], publisher: str) -> None:
    """
        Saves an array of articles to a parquet file

        An array of Articles is converted to a pandas DataFrame to prepare for saving

        The following directory is created and the parquet file is saved to:

        /in_the_news/data/parsed/year/month/day/hour/publisher.parquet

        /year/day/month/hour/ comes from when the current time, which is when the article was scraped
    """
    # maybe get the path to save from based on input date folders from scraped folder
    dir_to_save = get_path_with_current_datetime('in_the_news', 'data/parsed')
    dir_to_save.mkdir(parents=True, exist_ok=True)
    # pandas may be unneccesary, might be better to directly use pyarrow
    df = pd.DataFrame([article for article in articles])
    df.to_parquet(Path.joinpath(dir_to_save, publisher + '.parquet'), engine='pyarrow')


# throws i/o error
def parse_articles_from_soup(soup: BeautifulSoup, publisher) -> List[Article]:
    """
        Parses all articles from an RSS feeds into a list of Article objects and outputs that list

        RSS feed is input as a BeautifulSoup and and the publisher is added to the Article
    """
    items = soup.find_all('item')

    articles = []

    for item in items:
        article = article_factory(item, publisher)
        articles.append(article)

    return articles


# throws i/o error
def parse_scraped_data(directory: Path) -> None:
    """Parses all .xml files in a given directory and saves them to a seperate directory as .parquet files"""
    for file in directory:
        if str(file).endswith('xml'):
            with open(file) as f:
                soup = BeautifulSoup(f, 'xml')
                articles = parse_articles_from_soup(soup, file.stem)
                save_parsed_articles(articles, file.stem)


if __name__ == "__main__":
    # this should find most recently scraped folder or generate a path based on datetime input
    dir_to_parse = Path(__file__).parent.parent.joinpath('data/scraped/2022/05/08/22')
    parse_scraped_data(dir_to_parse.glob('*'))


    # parse 
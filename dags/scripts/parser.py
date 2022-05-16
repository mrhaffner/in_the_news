import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path
from typing import List
from airflow.models import Variable
from scripts.utilities.article import Article, article_factory
from scripts.utilities.pathing import add_datetime_to_path


def _save_parsed_articles(articles: List[Article], publisher: str) -> None:
    """
    Converts an array of articles to a dataframe then saves to a parquet file.

    Parquet file is saved to:
    /in_the_news/data/parsed/year/month/day/hour/publisher.parquet
    /year/day/month/hour/ comes from when the current time, which is when the article was scraped
    """
    scraped_dir_root = Path(Variable.get('base_dir')).joinpath('data/parsed')
    dir_to_save = add_datetime_to_path(scraped_dir_root, Variable.get('current_time'))
    dir_to_save.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame([article for article in articles])
    df.to_parquet(Path.joinpath(dir_to_save, publisher + '.parquet'), engine='pyarrow')


def _parse_articles_from_soup(soup: BeautifulSoup, publisher) -> List[Article]:
    """
    Parses all articles from an RSS feeds into a list of Article objects and outputs that list.
    RSS feed is input as a BeautifulSoup and and the publisher is added to the Article.
    """
    items = soup.find_all('item')
    articles = []

    for item in items:
        article = article_factory(item, publisher)
        articles.append(article)

    return articles


def _parse_scraped_data(directory: Path) -> None:
    """Parses all .xml files in a given directory and saves them to a seperate directory as .parquet files."""
    for file in directory:
        if str(file).endswith('xml'):
            with open(file) as f:
                soup = BeautifulSoup(f, 'xml')
                articles = _parse_articles_from_soup(soup, file.stem)
                _save_parsed_articles(articles, file.stem)


def parser() -> None:
    """Parses all .xml articles in a directory based on current_time passed from airflow and saves output as .parquet"""
    scraped_dir_root = Path(Variable.get('base_dir')).joinpath('data/scraped')
    dir_to_parse = add_datetime_to_path(scraped_dir_root, Variable.get('current_time'))
    _parse_scraped_data(dir_to_parse.glob('*'))
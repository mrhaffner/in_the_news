from dataclasses import dataclass
from bs4 import BeautifulSoup


@dataclass
class Article:
    """A scraped news article that has been parsed"""
    title: str
    pub_date: str
    url: str
    author: str
    publisher: str


def _create_title(article_soup: BeautifulSoup) -> str:
    """
        Takes an <item></item> soup and finds the the title tag

        Cleans and retuns text from title tag

        Returns empty string if there is no title tag
    """
    title = ''
    titles = article_soup.find_all('title')

    if len(titles) > 0:
        title = article_soup.title.get_text()

    return title.strip()


def _create_pub_date(article_soup: BeautifulSoup) -> str:
    """
        Takes an <item></item> soup and finds the the pubDate tag

        Cleans and retuns text from pubDate tag
        
        Returns empty string if there is no pubDate tag
    """
    pub_date = ''
    pub_dates = article_soup.find_all('pubDate')

    if len(pub_dates) > 0:
        pub_date = article_soup.pubDate.get_text()

    # optionally add date if blank?
    # convert to some datatime standard?

    return pub_date.strip()
    

def _create_url(article_soup: BeautifulSoup) -> str:
    """
        Takes an <item></item> soup and finds the the link tag

        Cleans and retuns text from link tag
        
        Returns empty string if there is no link tag
    """
    url = ''
    urls = article_soup.find_all('link')

    if len(urls) > 0:
        url = article_soup.link.get_text()

    return url.strip()


def _create_author(article_soup: BeautifulSoup) -> str:
    """
        Takes an <item></item> soup and finds the the dc:creator or author tag

        Cleans and retuns text from the tag (prefentially uses dc:creator tag)
        
        Returns empty string if there is no dc:creator or author tag
    """
    author = ''
    creators = article_soup.find_all('creator')

    if len(creators) > 0:
        author = article_soup.creator.get_text()

    authors = article_soup.find_all('author')

    if author == '' and len(authors) > 0:
        author = article_soup.author.get_text()

    return author.strip()


def article_factory(article_soup: BeautifulSoup, publisher: str) -> Article:
    """Creates and Returns an Article dataclass from an <item></item> soup and publisher"""
    title = _create_title(article_soup)
    pub_date = _create_pub_date(article_soup)
    url = _create_url(article_soup)
    author = _create_author(article_soup)

    return Article(title, pub_date, url, author, publisher)
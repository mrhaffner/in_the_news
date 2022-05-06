from dataclasses import dataclass

@dataclass
class Article:
    title: str
    pub_date: str #?
    url: str
    author: str
    publisher: str


def _create_title(article_soup):
    title = ''

    titles = article_soup.find_all('title')
    if len(titles) > 0:
        title = article_soup.title.get_text()

    return title.strip()


def _create_pub_date(article_soup):
    pub_date = ''

    pub_dates = article_soup.find_all('pubDate')
    if len(pub_dates) > 0:
        pub_date = article_soup.pubDate.get_text()

    #optionally add date if blank?
    # convert to some datatime?

    return pub_date.strip()
    

def _create_url(article_soup):
    url = ''

    urls = article_soup.find_all('link')
    if len(urls) > 0:
        url = article_soup.link.get_text()

    return url.strip()


def _create_author(article_soup):
    author = ''

    creators = article_soup.find_all('creator')
    if len(creators) > 0:
        author = article_soup.creator.get_text()

    authors = article_soup.find_all('author')
    if author == '' and len(authors) > 0:
        author = article_soup.author.get_text()

    return author.strip()

def article_factory(article_soup, publisher):
    title = _create_title(article_soup)
    pub_date = _create_pub_date(article_soup)
    url = _create_url(article_soup)
    author = _create_author(article_soup)

    return Article(title, pub_date, url, author, publisher)
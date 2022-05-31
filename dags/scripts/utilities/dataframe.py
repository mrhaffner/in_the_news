import pandas as pd

from pathlib import Path
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def get_articles_df_from_path(dir: Path) -> pd.DataFrame:
    '''
    Creates a dataframe containing a list of news articles from a path containing multiple Parquet files

    Ouput dataframe will have columns:
        title: str (article title)
        pub_date: str (date article was published)
        url: str (link to article)
        author: str
        publisher: str
    '''
    path_to_parquet = Path(__file__).parent.parent.joinpath(dir)
    articles_df = pd.read_parquet(path_to_parquet, engine="pyarrow")
    return articles_df


def _classify_leaning(publisher: str) -> str:
    '''Returns the political leaning of a given publisher'''
    csv_path = Path(__file__).parent.parent.joinpath('config/news_sites.csv')
    df = pd.read_csv(csv_path)
    leaning = df[df['id'] == publisher]['leaning'].values
    
    if len(leaning) > 0:
        return leaning[0]
    else:
        return ''


def _get_sentiment(text: str) -> float:
    '''
    Returns the sentiment score for a given String. Score ranges from -1 to 1.
    Positive scores indicate positive sentiment.
    Negative scores indicate negative sentiment.
    Neutral sentiment is indicated by 0.
    '''
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(text)['compound']


def classify_sentiment(articles_df: pd.DataFrame) -> pd.DataFrame:
    '''
    Adds sentiment and political leaning columns to a dataframe

    articles_df needs columns:
        title: str (sentiment will be analyzed)
        publisher: str (to get political leaning)

    output dataframe will have new columns:
        sentiment: float (range from -1 to 1)
        leaning: str (values 'right' or 'left' representing political leaning)
    '''
    articles_df['sentiment'] = articles_df['title'].apply(_get_sentiment)
    articles_df['leaning'] = articles_df['publisher'].apply(_classify_leaning)
    return articles_df


def create_sentiment_df(dir: Path) -> pd.DataFrame:
    '''
    Creates a dataframe of news articles from parquet files in dir. Adds 
    sentiment scores and political leaning to dataframe.

    Ouput dataframe will have columsn:
        title: str (article title)
        pub_date: str (date article was published)
        url: str (link to article)
        author: str
        publisher: str
        sentiment: float (range from -1 to 1)
        leaning: str (values 'right' or 'left' representing political leaning)
    '''
    articles_df = get_articles_df_from_path(dir)
    classified_df = classify_sentiment(articles_df)
    return classified_df
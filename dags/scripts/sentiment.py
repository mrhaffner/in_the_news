import datetime
import pandas as pd

from pathlib import Path
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from airflow.models import Variable
from airflow.providers.sqlite.hooks.sqlite import SqliteHook
from scripts.utilities.dataframe import classify_leaning, get_articles_df_from_path 
from scripts.utilities.pathing import add_datetime_to_path


def _get_sentiment(text: str) -> float:
    '''
    Returns the sentiment score for a given String. Score ranges from -1 to 1.
    Positive scores indicate positive sentiment.
    Negative scores indicate negative sentiment.
    Neutral sentiment is indicated by 0.
    '''
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(text)['compound']


def _classify_sentiment(articles_df: pd.DataFrame) -> pd.DataFrame:
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
    articles_df['leaning'] = articles_df['publisher'].apply(classify_leaning)
    return articles_df


def sentimentizer() -> None:
    '''Gathers means sentiment data from all, left leaning, and right leaning media and saves to database.'''
    parsed_dir_root = Path(Variable.get('base_dir')).joinpath('data/parsed')
    parsed_dir = add_datetime_to_path(parsed_dir_root, Variable.get('current_time'))
    articles_df = get_articles_df_from_path(parsed_dir)
    classified_df = _classify_sentiment(articles_df)
    leaning_mean_df = classified_df.groupby('leaning').mean()

    sqlite_hook = SqliteHook(sqlite_conn_id='news_db')
    rows = [(str(datetime.datetime.utcnow()), leaning_mean_df.loc['left']['sentiment'], leaning_mean_df.loc['right']['sentiment'], articles_df['sentiment'].mean())]
    target_fields = ['datetime', 'left_mean_sentiment', 'right_mean_sentiment', 'all_mean_sentiment']
    sqlite_hook.insert_rows(table='Sentiment', rows=rows, target_fields=target_fields, reaplce=True)
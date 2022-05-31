import datetime

from pathlib import Path
from airflow.models import Variable
from airflow.providers.sqlite.hooks.sqlite import SqliteHook
from scripts.utilities.dataframe import create_sentiment_df
from scripts.utilities.pathing import add_datetime_to_path


def sentimentizer() -> None:
    '''Gathers mean sentiment data from all, left leaning, and right leaning media and saves to database.'''
    parsed_dir_root = Path(Variable.get('base_dir')).joinpath('data/parsed')
    parsed_dir = add_datetime_to_path(parsed_dir_root, Variable.get('current_time'))
    classified_df = create_sentiment_df(parsed_dir)
    leaning_mean_df = classified_df.groupby('leaning').mean()

    sqlite_hook = SqliteHook(sqlite_conn_id='news_db')
    rows = [(str(datetime.datetime.utcnow()), leaning_mean_df.loc['left']['sentiment'], leaning_mean_df.loc['right']['sentiment'], classified_df['sentiment'].mean())]
    target_fields = ['datetime', 'left_mean_sentiment', 'right_mean_sentiment', 'all_mean_sentiment']
    sqlite_hook.insert_rows(table='Sentiment', rows=rows, target_fields=target_fields, replace=True)
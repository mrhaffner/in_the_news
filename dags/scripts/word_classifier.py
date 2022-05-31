import datetime
import pandas as pd
import string

from airflow.models import Variable
from airflow.providers.sqlite.hooks.sqlite import SqliteHook
from collections import Counter
from nltk import RegexpTokenizer
from nltk.corpus import stopwords
from pathlib import Path
from scripts.utilities.dataframe import create_sentiment_df 
from scripts.utilities.pathing import add_datetime_to_path


def _remove_punctuation(text):
    return ''.join([w for w in text if w not in string.punctuation])


def _remove_stopwords(words):
    return [word for word in words if word not in stopwords.words('english')]


def _tokenize_articles_df(df: pd.DataFrame) -> pd.DataFrame:
    # create new column with cleaned title
    df['cleaned'] = df['title'].apply(lambda x: _remove_punctuation(x))
    df['cleaned'] = df['cleaned'].apply(lambda x: x.lower())
    # create tokens
    tokenizer = RegexpTokenizer(r'\w+')
    df['tokens'] = df['cleaned'].apply(lambda x: tokenizer.tokenize(x))
    # remove stop words
    df['tokens'] = df['tokens'].apply(lambda x: _remove_stopwords(x))
    return df


def _add_counter_df(df: pd.DataFrame) -> pd.DataFrame:
    # create a counter
    df['counter'] = df['tokens'].apply(lambda x: Counter(x))
    return df


def  _get_aggregate_counter(df: pd.DataFrame) -> Counter:
    counter_list = list(df['counter'])
    agg_count = Counter()

    for counter in counter_list:
        agg_count.update(counter)
    
    return agg_count


def word_classifier() -> None:
    parsed_dir_root = Path(Variable.get('base_dir')).joinpath('data/parsed')
    parsed_dir = add_datetime_to_path(parsed_dir_root, Variable.get('current_time'))

    # testing path
    #parsed_dir = Path("/Users/mrhaffner/Documents/Projects/in_the_news/data/parsed/2022/05/16/19")

    classified_df = create_sentiment_df(parsed_dir)
    tokenized_df = _tokenize_articles_df(classified_df)
    counter_df = _add_counter_df(tokenized_df)

    all_counter = _get_aggregate_counter(counter_df[counter_df['sentiment'] < -.05])
    left_counter = _get_aggregate_counter(
        counter_df[(counter_df['leaning'] == 'left') & (counter_df['sentiment'] < -.05)]
    )
    right_counter = _get_aggregate_counter(
        counter_df.loc[(counter_df['leaning'] == 'right') & (counter_df['sentiment'] < -.05)]
    )

    sqlite_hook = SqliteHook(sqlite_conn_id='news_db')
    target_fields = [
        'datetime',
        'all_word_1',
        'all_word_2',
        'all_word_3',
        'left_word_1',
        'left_word_2',
        'left_word_3',
        'right_word_1',
        'right_word_2',
        'right_word_3'
    ]
    rows = [(
        str(datetime.datetime.utcnow()),
        all_counter.most_common(3)[0][0],
        all_counter.most_common(3)[1][0],
        all_counter.most_common(3)[2][0],
        left_counter.most_common(3)[0][0],
        left_counter.most_common(3)[1][0],
        left_counter.most_common(3)[2][0],
        right_counter.most_common(3)[0][0],
        right_counter.most_common(3)[1][0],
        right_counter.most_common(3)[2][0],
    )]
    sqlite_hook.insert_rows(table='Unhappy_words', rows=rows, target_fields=target_fields, replace=True)
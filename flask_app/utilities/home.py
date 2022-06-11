import sqlite3

from flask_app.db import get_db
from typing import Dict, List, TypedDict
from werkzeug.exceptions import abort


class Sentiment(TypedDict):
    left_mean_sentiment: str
    right_mean_sentiment: str
    all_mean_sentiment: str


class Mood(TypedDict):
    left: str
    right: str
    all: str


class Trend(TypedDict):
    left: str
    right: str
    all: str


def get_second_latest_sentiment() -> List[Sentiment]:
    '''
    Fetches most recent 2 sentiment data from database.
    Returns those rows as a list of dicts. 0 index being most recent.
    Abort 404 if no records are returned from database.
    '''
    sql_rows = (
        get_db()
        .execute(
            "SELECT left_mean_sentiment, right_mean_sentiment, all_mean_sentiment"
            " FROM Sentiment"
            " ORDER BY datetime DESC LIMIT 2",
        )
        .fetchall()
    )


    if sql_rows is None:
        abort(404, "No sentiment record found!")

    # index 0 is the most recent
    return sql_rows_to_list(sql_rows)


def sql_rows_to_list(sql_rows: List[sqlite3.Row]) -> List[Sentiment]:
    '''Takes a list of sql_row object and converts it to a list of sentiment dictionaries.'''
    return [sql_row_to_sentiment(s) for s in sql_rows]


def sql_row_to_sentiment(sql: sqlite3.Row) -> Sentiment:
    '''Converts one sql_row into a sentiment dictionary.'''
    return {
            'left_mean_sentiment': float(sql['left_mean_sentiment']), 
            'right_mean_sentiment': float(sql['right_mean_sentiment']), 
            'all_mean_sentiment': float(sql['all_mean_sentiment'])
            }    


def get_moods_from_sentiment(sentiment: Sentiment, adjustment=False) -> Mood:
    '''Creates and returns a dictionary with moods for each sentiment category.'''
    right = get_mood_word(float_to_percent(sentiment['right_mean_sentiment']), "right", adjustment)
    left = get_mood_word(float_to_percent(sentiment['left_mean_sentiment']), "left", adjustment)
    all = get_mood_word(float_to_percent(sentiment['all_mean_sentiment']), "all", adjustment)
    print(right, left, all)
    return {'right': right, 'left': left, 'all': all}


# represents adjusted sentiment scores
sentiment = {
    "ecstatic": [-2,-5,-4],
    "up-beat": [-7,-11,-8],
    "indifferent": [-9,-15,-10],
    "annoyed": [-13,-20,-15]
}


# news_type key for sentiment dictionary
adjust = {
    "left": 0,
    "right": 1,
    "all": 2
}


def get_mood_word(score: int, news_type: str, adjustment=False) -> str:
    '''
    Takes in a sentiment score from 100 to -100 and returns a text representationg of that score.
    May apply an adjustment to the score based on type.
    '''
    if score > (sentiment["ecstatic"][adjust[news_type]] if adjustment else 10):
        return "ecstatic"
    elif score > (sentiment["up-beat"][adjust[news_type]] if adjustment else 2):
        return "up-beat"
    elif score > (sentiment["indifferent"][adjust[news_type]] if adjustment else -2):
        return "indifferent"
    elif score > (sentiment["annoyed"][adjust[news_type]] if adjustment else -10):
        return "annoyed"
    else:
        return "seething"


def float_dict_to_percent(dict: Dict[str, float]) -> Dict[str, float]:
    '''
    Takes in a dictionary where all values are floats.
    Creates a new dictionary with the same keys where all values are converted to percentage with 0 decimals.
    '''
    new_dict = {}
    for key in dict:
        new_dict[key] = float_to_percent(dict[key])
    return new_dict


def float_to_percent(n: float) -> int:
    '''Converts a float to a percentage. Rounds to 0 decimal places.'''
    return int(round(float(n) * 100, 0))


def get_sentiment_trend(sentiments: List[Sentiment]) -> Trend:
    '''
    Creats a trend dictionary from a list of 2 sentiment dictionaries.
    Contains a trend direction for each sentiment category.
    '''
    trend = {}
    trend['left'] = get_trend(sentiments[0]['left_mean_sentiment'], sentiments[1]['left_mean_sentiment'])
    trend['all'] = get_trend(sentiments[0]['all_mean_sentiment'], sentiments[1]['all_mean_sentiment'])
    trend['right'] = get_trend(sentiments[0]['right_mean_sentiment'], sentiments[1]['right_mean_sentiment'])
    return trend


def get_trend(most_recent: float, second_recent: float) -> str:
    '''
    Takes in two sentiment scores and outputs a string indicating whether the scores are increasing,
    decreasing or staying the same.
    '''
    if float_to_percent(most_recent) > float_to_percent(second_recent):
        return "up"
    elif float_to_percent(most_recent) < float_to_percent(second_recent):
        return "down"
    else:
        return "none"


def get_unhappy_words() -> sqlite3.Row:
    '''
    Fetches most recent uunhappy words from database.
    Abort 404 if no records are returned from database.
    '''
    sql_row = (
        get_db()
        .execute(
            '''
            SELECT *
            FROM Unhappy_words
            ORDER BY datetime DESC LIMIT 1;
            '''
        )
        .fetchone()
    )

    if sql_row is None:
        abort(404, "No unhappy words record found!")

    return sql_row
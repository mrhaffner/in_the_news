from werkzeug.exceptions import abort
from flask_app.db import get_db


def get_second_latest_sentiment():
    '''
    Fetches most recent 2 sentiment data from database.
    Returns those rows as a list of dicts. 0 index being most recent.
    Abort 404 if no records are returned fromd database.
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


def sql_rows_to_list(sql):
    '''Takes a sql_row object and converts it to a list of dictionaries.'''
    return [sql_row_to_dict(s) for s in sql]


def sql_row_to_dict(sql):
    '''Converts one sql_row into a dictionary.'''
    return {
            'left_mean_sentiment': float(sql['left_mean_sentiment']), 
            'right_mean_sentiment': float(sql['right_mean_sentiment']), 
            'all_mean_sentiment': float(sql['all_mean_sentiment'])
            }    


def get_moods_from_sentiment(sentiment):
    '''Creates and returns a dictionary with moods for each sentiment category.'''
    right = get_mood_word(float(sentiment['right_mean_sentiment']))
    left = get_mood_word(float(sentiment['left_mean_sentiment']))
    all = get_mood_word(float(sentiment['all_mean_sentiment']))
    return {'right': right, 'left': left, 'all': all}


def get_mood_word(score):
    '''Takes in a sentiment score from 1 to -1 and returns a text representationg of that score.'''
    if score > .50:
        return "escstatic"
    elif score > .05:
        return "up-beat"
    elif score > -.05:
        return "indifferent"
    elif score > -.50:
        return "annoyed"
    else:
        return "seething"


def float_dict_to_percent(dict):
    '''
    Takes in a dictionary where all values are floats.
    Creates a new dictionary with the same keys where all values are converted to percentage with 0 decimals.
    '''
    new_dict = {}
    for key in dict:
        new_dict[key] = float_to_percent(dict[key])
    return new_dict


def float_to_percent(n):
    '''Converts a float to a percentage. Rounds to 0 decimal places.'''
    return int(round(float(n) * 100, 0))


def get_sentiment_trend(sentiments):
    '''
    Creats a trend dictionary from an array of 2 sentiment dictionaries.
    Contains a trend direction for each sentiment category.
    '''
    trend = {}
    trend['left'] = get_trend(sentiments[0]['left_mean_sentiment'], sentiments[1]['left_mean_sentiment'])
    trend['all'] = get_trend(sentiments[0]['all_mean_sentiment'], sentiments[1]['all_mean_sentiment'])
    trend['right'] = get_trend(sentiments[0]['right_mean_sentiment'], sentiments[1]['right_mean_sentiment'])
    return trend


def get_trend(most_recent, second_recent):
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
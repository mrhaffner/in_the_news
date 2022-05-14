
from flask import Blueprint
from flask import render_template
from werkzeug.exceptions import abort

from flask_app.db import get_db

bp = Blueprint("sentiment", __name__)


def get_mood_word(score):
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


def get_moods_from_sentiment(sentiment):
    right = get_mood_word(float(sentiment['right_mean_sentiment']))
    left = get_mood_word(float(sentiment['left_mean_sentiment']))
    all = get_mood_word(float(sentiment['all_mean_sentiment']))
    return {'right': right, 'left': left, 'all': all}


def float_dict_to_percent(dict):
    for key in dict:
        dict[key] = int(round(float(dict[key]) * 100, 0))
    return dict


def get_second_latest_sentiment():
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


def sql_row_to_dict(sql):
    return {'left_mean_sentiment': float(sql['left_mean_sentiment']), 'right_mean_sentiment': float(sql['right_mean_sentiment']), 'all_mean_sentiment': float(sql['all_mean_sentiment'])}    


def sql_rows_to_list(sql):
    return [sql_row_to_dict(s) for s in sql]


def get_trend(most_recent, second_recent):
    if most_recent > second_recent:
        return "up"
    elif most_recent < second_recent:
        return "down"
    else:
        return "none"


def get_sentiment_trend(sentiments):
    trend = {}
    trend['left'] = get_trend(sentiments[0]['left_mean_sentiment'], sentiments[1]['left_mean_sentiment'])
    trend['all'] = get_trend(sentiments[0]['all_mean_sentiment'], sentiments[1]['all_mean_sentiment'])
    trend['right'] = get_trend(sentiments[0]['right_mean_sentiment'], sentiments[1]['right_mean_sentiment'])
    return trend


@bp.route("/")
def index():
    sentiments = get_second_latest_sentiment()
    moods = get_moods_from_sentiment(sentiments[0])
    perc_sentiment = float_dict_to_percent(sentiments[0])
    trend = get_sentiment_trend(sentiments)

    return render_template("sentiment/index.html", sentiment=perc_sentiment, moods=moods, trend=trend)
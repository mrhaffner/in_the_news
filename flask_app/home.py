
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


def get_latest_sentiment():
    sql_rows = (
        get_db()
        .execute(
            "SELECT left_mean_sentiment, right_mean_sentiment, all_mean_sentiment"
            " FROM Sentiment"
            " ORDER BY datetime DESC LIMIT 1",
        )
        .fetchone()
    )

    if sql_rows is None:
        abort(404, "No sentiment record found!")

    sentiment = {'left_mean_sentiment': sql_rows['left_mean_sentiment'], 'right_mean_sentiment': sql_rows['right_mean_sentiment'], 'all_mean_sentiment': sql_rows['all_mean_sentiment']}

    return sentiment


@bp.route("/")
def index():
    sentiment = get_latest_sentiment()
    moods = get_moods_from_sentiment(sentiment)
    perc_sentiment = float_dict_to_percent(sentiment)

    return render_template("sentiment/index.html", sentiment=perc_sentiment, moods=moods)
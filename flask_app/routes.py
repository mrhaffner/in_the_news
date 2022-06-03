
from flask import Blueprint
from flask import render_template
from flask_app.utilities.home import get_second_latest_sentiment, get_moods_from_sentiment, float_dict_to_percent, get_sentiment_trend, get_unhappy_words


bp = Blueprint("sentiment", __name__)

@bp.route("/")
def index():
    '''Creates the index route that displays sentiment data'''
    sentiments = get_second_latest_sentiment()
    moods = get_moods_from_sentiment(sentiments[0])
    perc_sentiment = float_dict_to_percent(sentiments[0])
    trend = get_sentiment_trend(sentiments)
    words = get_unhappy_words()

    return render_template("sentiment/index.html", sentiment=perc_sentiment, moods=moods, trend=trend, words=words)
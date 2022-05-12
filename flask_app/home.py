
from flask import Blueprint
from flask import render_template
from werkzeug.exceptions import abort

from flask_app.db import get_db

bp = Blueprint("sentiment", __name__)


def get_latest_sentiment():
    sentiment = (
        get_db()
        .execute(
            "SELECT left_mean_sentiment, right_mean_sentiment, all_mean_sentiment"
            " FROM Sentiment"
            " ORDER BY datetime DESC LIMIT 1",
        )
        .fetchone()
    )

    if sentiment is None:
        abort(404, "No sentiment record found!")

    return sentiment


@bp.route("/")
def index():
    sentiment = get_latest_sentiment()
    return render_template("sentiment/index.html", sentiment=sentiment)
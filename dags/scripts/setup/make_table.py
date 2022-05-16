import sqlite3


def _make_table() -> None:
    """Creates a sentiment sqlite table"""
    conn = sqlite3.connect('news.db') # ????
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS Sentiment
        (datetime TEXT PRIMARY KEY NOT NULL,
        left_mean_sentiment TEXT NOT NULL,
        right_mean_sentiment TEXT NOT NULL,
        all_mean_sentiment TEXT NOT_NULL)
    ''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    _make_table()
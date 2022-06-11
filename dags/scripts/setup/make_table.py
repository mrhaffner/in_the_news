import sqlite3


def _make_table() -> None:
    """Creates a sentiment sqlite table"""
    conn = sqlite3.connect('news.db') # ????
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS Sentiment
        (
            datetime TEXT PRIMARY KEY NOT NULL,
            left_mean_sentiment REAL NOT NULL,
            right_mean_sentiment REAL NOT NULL,
            all_mean_sentiment REAL NOT_NULL
        );
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS Unhappy_words
        (
            datetime TEXT PRIMARY KEY NOT NULL,
            all_word_1 TEXT NOT NULL,
            all_word_2 TEXT NOT NULL,
            all_word_3 TEXT NOT NULL,
            left_word_1 TEXT NOT NULL,
            left_word_2 TEXT NOT NULL,
            left_word_3 TEXT NOT NULL,
            right_word_1 TEXT NOT NULL,
            right_word_2 TEXT NOT NULL,
            right_word_3 TEXT NOT NULL
        );
    ''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    _make_table()
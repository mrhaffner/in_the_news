CREATE TABLE IF NOT EXISTS Sentiment (
    datetime TEXT PRIMARY KEY NOT NULL,
    left_mean_sentiment TEXT NOT NULL,
    right_mean_sentiment TEXT NOT NULL,
    all_mean_sentiment TEXT NOT_NULL
);

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
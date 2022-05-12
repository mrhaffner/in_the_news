CREATE TABLE IF NOT EXISTS Sentiment (
    datetime TEXT PRIMARY KEY NOT NULL,
    left_mean_sentiment TEXT NOT NULL,
    right_mean_sentiment TEXT NOT NULL,
    all_mean_sentiment TEXT NOT_NULL
);
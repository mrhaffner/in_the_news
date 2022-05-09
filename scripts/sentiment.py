import datetime
import pandas as pd
import sqlite3
from pathlib import Path
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def classify_leaning(publisher):
    csv_path = Path(__file__).parent.joinpath('config/news_sites.csv')
    df = pd.read_csv(csv_path)
    leaning = df[df['id'] == publisher]['leaning'].values
    
    if len(leaning) > 0:
        return leaning[0]
    else:
        return ''


def get_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(text)['compound']


def create_mean_df(articles_df):
    total_mean_df = articles_df['sentiment'].mean()
    leaning_mean_df = articles_df.groupby('leaning').mean()

    sent_data = {'datetime': [datetime.datetime.now()], 'left_mean_sentiment': [leaning_mean_df.loc['left']['sentiment']], 'right_mean_sentiment': [leaning_mean_df.loc['right']['sentiment']], 'all_mean_sentiment': [total_mean_df]}
    sentiment_df = pd.DataFrame(data=sent_data)
    sentiment_df.set_index('datetime', inplace = True)
    return sentiment_df


def classify_hourly_sentiment(dir_to_parse):
    articles_df = pd.read_parquet(dir_to_parse, engine="pyarrow")
    articles_df['sentiment'] = articles_df['title'].apply(get_sentiment)
    articles_df['leaning'] = articles_df['publisher'].apply(classify_leaning)

    sentiment_df = create_mean_df(articles_df)
    return sentiment_df


if __name__ == "__main__":
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS Sentiment
        (datetime TEXT PRIMARY KEY NOT NULL,
        left_mean_sentiment TEXT NOT NULL,
        right_mean_sentiment TEXT NOT NULL,
        all_mean_sentiment TEXT NOT_NULL)
    ''')

    path_to_parquet = Path(__file__).parent.parent.joinpath('data/parsed/2022/05/08/22')
    df = classify_hourly_sentiment(path_to_parquet)
    df.to_sql(name='Sentiment', con=conn, if_exists='append')

    conn.commit()
    conn.close()
    #percent negative articles
    #percent positive articles
    #visual percent neg/percent pos

    #want to save a snapshot
    # mildly positive, very positive, neutral, mildly negative, very negative
    # snapshot will have statistics for each news source, all news sources, and by political leanings
    #probably want to take all parquet files into a single df for this analysis
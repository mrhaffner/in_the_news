import datetime
import pandas as pd
import sqlite3
from pathlib import Path
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# create df from parquet file
# use textblob on description of df to create polarity colum
# get mean polarity of polarity column
# save that polarity to somewhere


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
    df = pd.read_parquet(path_to_parquet, engine="pyarrow")
    df['sentiment'] = df['title'].apply(get_sentiment)

    df['leaning'] = df['publisher'].apply(classify_leaning)
    
    df3 = df['sentiment'].mean()
    print(df3)

    df4 = df.groupby('leaning').mean()

    d = {'datetime': [datetime.datetime.now()], 'left_mean_sentiment': [df4.loc['left']['sentiment']], 'right_mean_sentiment': [df4.loc['right']['sentiment']], 'all_mean_sentiment': [df3]}
    df = pd.DataFrame(data=d)
    df.set_index('datetime', inplace = True)
    print(df)
    df.to_sql(name='Sentiment', con=conn, if_exists='append')
    conn.commit()
    sql_df = pd.DataFrame(cur.fetchall(), columns = ['datetime', 'left_mean_sentiment', 'right_mean_sentiment', 'all_mean_sentiment'])
    print(sql_df)

  
    conn.close()
    #percent negative articles
    #percent positive articles
    #visual percent neg/percent pos

    #want to save a snapshot
    # mildly positive, very positive, neutral, mildly negative, very negative
    # snapshot will have statistics for each news source, all news sources, and by political leanings
    #probably want to take all parquet files into a single df for this analysis
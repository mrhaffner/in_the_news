import datetime
import pandas as pd
import sqlite3
from pathlib import Path
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def get_articles_df_from_path(dir: Path) -> pd.DataFrame:
    '''
        Creates a dataframe containing a list of news articles from a path containing multiple Parquet files

        Ouput dataframe will have colums:
            title: str (article title)
            pub_date: str (date article was published)
            url: str (link to article)
            author: str
            publisher: str
    '''
    path_to_parquet = Path(__file__).parent.parent.joinpath(dir)
    articles_df = pd.read_parquet(path_to_parquet, engine="pyarrow")
    return articles_df


def classify_leaning(publisher: str) -> str:
    '''Returns the political leaning of a given publisher'''
    csv_path = Path(__file__).parent.joinpath('config/news_sites.csv')
    df = pd.read_csv(csv_path)
    leaning = df[df['id'] == publisher]['leaning'].values
    
    if len(leaning) > 0:
        return leaning[0]
    else:
        return ''


def get_sentiment(text: str) -> float:
    '''
        Returns the sentiment score for a given String. Score ranges from -1 to 1.
        Positive scores indicate positive sentiment.
        Negative scores indicate negative sentiment.
        Neutral sentiment is indicated by 0.
    '''
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(text)['compound']


def classify_sentiment(articles_df: pd.DataFrame) -> pd.DataFrame:
    '''
         Adds sentiment and political leaning columns to a dataframe

         articles_df needs columns:
            title: str (sentiment will be analyzed)
            publisher: str (to get political leaning)

        output dataframe will have new columns:
            sentiment: float (range from -1 to 1)
            leaning: str (values 'right' or 'left' representing political leaning)
    '''
    articles_df['sentiment'] = articles_df['title'].apply(get_sentiment)
    articles_df['leaning'] = articles_df['publisher'].apply(classify_leaning)
    return articles_df


def create_mean_df(articles_df: pd.DataFrame) -> pd.DataFrame:
    '''
        Returns a dataframe consisting of mean sentiments scores from the input articles dataframe

        The Articles Dataframe needs columns:
            sentiment: float (range from -1 to 1)
            leaning: str (values 'right' or 'left' representing political leaning)

        Outputs 1 row summary dataframe with columns:
            datetime: str
            left_mean_sentiment: float (range from -1 to 1)
            right_mean_sentiment: float (range from -1 to 1)
            all_mean_sentiment: float (range from -1 to 1)
    '''
    total_mean_df = articles_df['sentiment'].mean()
    leaning_mean_df = articles_df.groupby('leaning').mean()

    sent_data = {'datetime': [datetime.datetime.now()], 'left_mean_sentiment': [leaning_mean_df.loc['left']['sentiment']], 'right_mean_sentiment': [leaning_mean_df.loc['right']['sentiment']], 'all_mean_sentiment': [total_mean_df]}
    sentiment_df = pd.DataFrame(data=sent_data)
    sentiment_df.set_index('datetime', inplace = True)
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

    articles_df = get_articles_df_from_path('data/parsed/2022/05/08/22') # will need to figure out how to change input here
    classified_df = classify_sentiment(articles_df)
    sentiment_df = create_mean_df(classified_df)

    print(sentiment_df)
    sentiment_df.to_sql(name='Sentiment', con=conn, if_exists='append')

    conn.commit()
    conn.close()

    #percent negative articles
    #percent positive articles
    #visual percent neg/percent pos

    #want to save a snapshot
    # mildly positive, very positive, neutral, mildly negative, very negative
    # snapshot will have statistics for each news source, all news sources, and by political leanings
    #probably want to take all parquet files into a single df for this analysis
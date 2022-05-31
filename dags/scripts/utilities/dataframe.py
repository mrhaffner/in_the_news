import pandas as pd
from pathlib import Path


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
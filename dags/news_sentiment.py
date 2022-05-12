from datetime import datetime, timedelta, timezone
from pathlib import Path

from scripts.parser import parser
from scripts.scraper import scraper
from scripts.sentiment import sentimentizer

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.providers.sqlite.operators.sqlite import SqliteOperator


# Set variables for external python scripts
Variable.set('base_dir', Path(__file__).parent.parent)
Variable.set('current_time', datetime.now(timezone.utc))


with DAG(
    'sentiment_etl',
    default_args={
        'depends_on_past': False,
        'email': ['airflow@example.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    description='Get news sentiment',
    schedule_interval='@hourly',
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:

    t1 = PythonOperator(
        task_id='scrape_rss_feeds',
        python_callable=scraper,
    )

    t2 = PythonOperator(
        task_id='parse_rss_feeds',
        #depends_on_past=True,
        python_callable=parser,
    )

    t3 = PythonOperator(
        task_id='generate_rss_sentiment',
        #depends_on_past=True,
        python_callable=sentimentizer,
    )

    t1 >> t2 >> t3
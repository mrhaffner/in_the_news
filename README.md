Data Engineering Project

Scrapes News Websites to gather keywords for analysis

Setting up:
create virtual environment in /venv

Activate virtual environment:
source venv/bin/activate

Install packages:
pip install -r requirements.txt

Install airflow:
pip install "apache-airflow==2.2.3" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.2.3/constraints-no-providers-3.9.txt"

Set up airflow:
airflow db init
cd ~/ariflow
airflow users create \
 --username admin \
 --firstname FIRST_NAME \
 --lastname LAST_NAME \
 --role Admin \
 --email admin@example.org

open airflow.cfg and change dags_folder to point to project directory
dags_folder = path/to/project/in_the_news/dags

Set up the database:
python dags/scripts/setup/make_table.py

airflow webserver -D
go to http://localhost:8080

set up database connection path:
In airflow webbrowser, go to Admin tab then connections
Add new connections name = news, connection type = sqlite,
host = path/to/in_the_news/news.db

airflow scheduler -D

Run the tests:
python -m pytest -q scripts/tests/test_parser.py

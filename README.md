Data Engineering Project

Scrapes News Websites to gather keywords for analysis

Setting up:
create virtual environment in /venv

Activate virtual environment:
source venv/bin/activate

must have sqlite3 installed

Install packages:
pip install -r requirements.txt

Install airflow:
pip install "apache-airflow==2.2.3" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.2.3/constraints-no-providers-3.9.txt"

Set up airflow:
airflow db init
airflow users create \
 --username admin \
 --firstname FIRST_NAME \
 --lastname LAST_NAME \
 --role Admin \
 --email admin@example.org

open airflow.cfg and change dags_folder to point to project directory
dags_folder = path/to/project/in_the_news/dags

You may also want to set (hides the 30 example DAGS in webserver UI):
load_examples = False
$airflow db reset

Set up the database:
python dags/scripts/setup/make_table.py

set up database connection path (if the airflow meta db is ever reset, you will need to set this again):
airflow connections add 'news_db' \
 --conn-type 'sqlite' \
 --conn-host '/path/to/your/db/in_the_news/news.db'

Start the webserver if you wish to use the UI:
airflow webserver -D
go to http://localhost:8080

airflow scheduler -D

Run the tests:
python -m pytest -q scripts/tests/test_parser.py

Run the flask app in development mode:
export FLASK_APP=flask_app
export FLASK_ENV=development
flask run

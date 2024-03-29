## In The News

A simple ETL that gathers data hourly from news RSS feeds and analyzes sentiment.

~~Visit the Mood-O-Meter to see the media's current mood (spoiler - it is never positive) (not mobile optimized):~~

~~https://moodometer.mattrhaffner.com/~~

The project is no longer live!

![alt text](project_diagram.png)

## Purpose:

- Practice writing Python with proper documentation, comments, and type hints
- Learn about using Apache Airflow for orchestrating data pipelines
- Explore the Pandas library for data manipulation
- Practice writing custom SQL
- Gain experience deploying a project on a linux server

## Set Up:

Requires python 3.9, pip, venv, and sqlite3.
After cloning the repository, cd into /in_the_news:

```sh
$ python3.9 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python3.9 -m nltk.downloader stopwords
```

Set up Airflow:

```sh
$ airflow db init
$ airflow users create \
 --username admin \
 --firstname FIRST_NAME \
 --lastname LAST_NAME \
 --role Admin \
 --email admin@example.org
```

Open airflow.cfg in the airflow folder and update dags_folder property (found in first section: [core]):

```sh
$ nano ~/airflow/airflow.cfg
dags_folder = path/to/project/in_the_news/dags
```

You may also want to update load_examples property to hide the 30 example DAGS in the webserver UI (found in first section: [core]):

```sh
load_examples = False
```

You may need to reset the airflow meta database to hide the example dags:

```sh
$ airflow db reset
```

Set up the project database:

```sh
$ python dags/scripts/setup/make_table.py
```

Set up database connection path (if the airflow meta db is ever reset, you will need to set this again):

```sh
$ airflow connections add 'news_db' \
 --conn-type 'sqlite' \
 --conn-host '/path/to/your/db/in_the_news/news.db'
```

Start the scheduler and webserver in daemon mode:

```sh
$ airflow scheduler -D
$ airflow webserver -D
```

Visit http://localhost:8080 in your web browser and login to use the UI and start the DAG.

If the scheduler decides to stop working in daemon mode after activation, cd into your airflow home folder and run:

```sh
$ sudo rm airflow-scheduler.err airflow-scheduler.pid
$ airflow scheduler -D
```

Run the tests:

```sh
$ python -m pytest -q scripts/tests/test_parser.py
```

Run the flask app in development mode (this needs two succesful runs of the ETL for datapoints):

```sh
$ export FLASK_APP=flask_app
$ export FLASK_ENV=development
$ flask run
```

Visit the flask app in your web browser at http://localhost:5000

## Deployment:

I deployed my project to the lowest tier Digital Ocean droplet running on Ubuntu 20.04. This tier has 1 GB of working memory (Update: there is now a 
lower tier of droplet with even less memory). More working memory would improve this project.  It is not possible to concurrently run Airflow, the 
Airflow web interface, and the project's webview (you may use one web interface with Airflow running). It is also not possible to run Airflow, the 
webview and concurrent DAGs.

Update: The ETL ran smoothly for a few months. After a fair amount of debugging, it seems that the 1GB of working memory is not always adequate anymore. This will cause the ETL to fail. Results will become stale without manually adjusting the ETL to skip a run that failed due to lack of memory. A simpler fix is just to pay for more working memory.  This was a project for learning, so I am likely to soon discontinue the live page rather than do continual manual adjustments or pay for a higher tier droplet.

I followed these instructions to set up a NGINX and uWSGI server to run the Flask app in production (you will need to use Python 3.9):
https://pythonforundergradengineers.com/flask-app-on-digital-ocean.html

Note that flaskapp.py and wsgi.py in the root directory serve as entry points for the production Flask app.

## Configuration:

The RSS feeds to be scraped are found in /dags/scripts/config/news_sites.csv

It is possible to add more RSS feeds to this file. I suggest adding an equal number of right and left leaning websites. It is possible that additional RSS feeds will not be parsed properly - make sure to check the data saved to the .parquet files to ensure they are compatible.

## Potential improvements:

- More tests!
- Mobile optimization
- A way to filter / remove irrelevant words from the "unhappy words feed"

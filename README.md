## In The News

A simple ETL that gathers data from news RSS feeds and analyzes their sentiment.

Visit the Mood-O-Meter to see the media's current mood:

https://moodometer.mattrhaffner.com/

### Set Up:

Requires python 3.9 and sqlite3.
After cloning the repository, cd into /in_the_news:

```sh
$ python3.9 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Set up airflow:

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

You may also want to update load_examples property to hide the 30 example DAGS in webserver UI (found in first section: [core]):

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

### Deployment:

I deployed my project to the lowest tier DigitalOcean droplet running on Ubuntu 20.04. This tier has 1 GB of memory which barely cuts it for everything to run. For instance, I had set up airflow with the webserver running, and there was not enough memory to install some of the packages for the flask app. (Note there is now a lower tier of droplet with even less memory)

I followed these instructions to set up a NGINX and uWSGI server to run the flask app in production (you will need to use python 3.9):
https://pythonforundergradengineers.com/flask-app-on-digital-ocean.html

Note that flaskapp.py and wsgi.py in the root directory serve as entry points for the production flask app.

### Configuration:

The RSS feeds to be scraped are found in /dags/scripts/config/news_sites.csv

It is possible to add more RSS feeds to this file. I suggest adding an equal number of right and left leaning websites. It is possible that additional RSS feeds will not be parsed properly - make sure to check the data saved to the .parquet files to ensure they are compatible.

# facebook-birthday-extractor
Realistic scraper that extracts your Facebook friends' birthdays in a calendar format.
Hopefully, it's going to work for a long time, until Facebook decides to do an UI change.

## Setup

1. Create a new venv with `python -m venv env`
2. Install the requirements with `pip install -r requirements.txt`
3. Install the project as editable with `pip install -e .` (yes, with period)
4. `cd src/`
5. `scrapy crawl facebook`
6. Enjoy :)

Optional steps (for running under Docker/Airflow):

7. `docker-compose up airflow-init` - initializes the DB and creates a default user, `airflow`, with the password `airflow`.

## Running under Airflow

Airflow is a blanao task scheduler which can create DAGs (directed acyclic graphs) of tasks.

> Please run `docker-compose up airflow-init` for the first time, for upgrading the DB models and creating an user account that grants access to Airflow's interface.
- `docker-compose up airflow-webserver airflow-worker airflow-scheduler flower` - fires up the essential services to make Airflow run.

## Google Chrome container

Almost copy-pasted @stephen-fox's guide.
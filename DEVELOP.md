# Developer instructions

**This file was generated automatically**

## Project Structure
A skeleton Flask app was automatically configured by pyreleaser_io for:

* A _large_ application, based on
  https://flask.palletsprojects.com/en/1.1.x/patterns/packages/#larger-applications
* pytest unit testing, based on
  https://www.patricksoftwareblog.com/testing-a-flask-application-using-pytest/
* `uwsgi` support based on
  https://flask.palletsprojects.com/en/1.1.x/deploying/uwsgi/

## Running a development server

```shell
FLASK_APP=artifactory_cloud_proxy pipenv run flask run
```

## Running a production (uwsgi) server

```shell
pipenv run uwsgi -s /tmp/artifactory_cloud_proxy.sock --manage-script-name --mount /artifactory_cloud_proxy=artifactory_cloud_proxy:app
```

Reference: https://flask.palletsprojects.com/en/1.1.x/deploying/uwsgi/

## Testing
Approach based on:

```shell
FLASK_APP=artifactory_cloud_proxy pipenv run pytest
```

## Getting a shell
```shell
pipenv shell
```
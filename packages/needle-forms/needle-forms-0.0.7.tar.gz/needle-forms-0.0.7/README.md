# Needle Forms

It is a project containing classes to make easy handling GCP resources such as Datastore, PubSub and CloudSql.

* [python 3.7.3](https://www.python.org/downloads/release/python-373/)
    * [pipenv](https://docs.pipenv.org/en/latest/install/#installing-pipenv) 
* [gcloud command line](https://cloud.google.com/sdk/install) 

## Install project dependencies

**On the project root folder**, execute the following command:

`pipenv install --dev --python ~/.pyenv/versions/3.7.3/bin/python`

Note: adjust the python path according to your environment

## Commands

* Clean python compiled files and cached data.
```
make clean
```
* Perform local tests
```
make test 
```
* Perform tests with coverage
```
make cov
```
* Perform lint on the files
```
make lint
```

* Perform black on the files
```
make black
```

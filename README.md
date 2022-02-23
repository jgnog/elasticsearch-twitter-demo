# Using Elasticsearch to search through tweets

The goal of this exercise is to use Elasticsearch full-text search capabilities
to search through a corpus of tweets. The Python script should perform the following
functions:

1. Extract recent tweets from a list of authors using the Twitter API
2. Ingest those tweets into an index in Elasticsearch
3. Accept user input for a given search term or phrase, issue a query to Elasticsearch
and return a list of matching tweets

## Preparing the Python environment

To complete this exercise, you will need two external libraries:

- requests: a library that helps you issue HTTP requests
- elasticsearch: the official Python Elasticsearch client library

These requirements are already defined in `requirements.txt`. The recommended
way to install these dependencies is to create a virtual environment and then
use `pip` to install the packages in the virtual environment.

Create the virtual environment with this command:

```
python3 -m venv venv
```

This will create a new folder `venv` that contains the files needed for the
virtual environment.

Activate the virtual environment.

In Linux and macOS:

```
source venv/bin/activate
```

In Windows classic command line:

`venv/Scripts/activate.bat`

In Windows PowerShell:

`venv/Scripts/Activate.ps1`

Now that you are inside the virtual environment, install the packages using
`pip`.

`pip install -r requirements.txt`

To test if everything is working, launch a Python interpreter and try importing
the two packages.

```
$ python
>>> import requests
>>> import elasticsearch
```

If you don't see any output, then everything is working as it should.

## Extracting tweets

The provided script in `main.py` already has all the code needed to extract
tweets via the Twitter API. The list of authors that will be searched in is
in the file `data_authors` where each line is a valid username. The provided
list contains authors known for tweeting about Data Analytics. Feel free to
add more.

To make the script work, you need to provide valid credentials for the Twitter
API authentication. To do that, create a new file named `config.ini` in this
folder. This file should have the following contents:

```
[TWITTER]
bearer_token = <your-bearer-token>
```

You should replace `<your-bearer-token>` with a valid Twitter API bearer token.

This file will be read by `main.py` and the bearer token will be used to
authenticate the API call.

## Indexing tweets in Elasticsearch

Once again, you will need to provide proper credentials to authenticate the
usage of the client library with your Elasticsearch server. Add a new section
to `config.ini` with the following content:

```
[ELASTIC]
cloud_id = <your-cloud-id>
apikey_id = <your-api-key-id>
apikey_key = <your-api-key>
```

The `main.py` script already creates an Elasticsearch object that you can use
to perform operations in the Elasticsearch server. Here are the lines of code
responsible for creating that object.

```
es = Elasticsearch(
    cloud_id=config['ELASTIC']['cloud_id'],
    api_key=(config['ELASTIC']['apikey_id'], config['ELASTIC']['apikey_key']),
)
```

Read [this
documentation](https://www.elastic.co/guide/en/elasticsearch/client/python-api/8.0/examples.html)
for an example on how to insert a document in an index.

The index name should be the one provided to your group. Your API key will only
be able to make changes to that index, so any operation on any other index or
creating a new index will fail.


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

```
venv/Scripts/activate.bat
```

In Windows PowerShell:

```
venv/Scripts/Activate.ps1
```

Now that you are inside the virtual environment, install the packages using
`pip`.

```
pip install -r requirements.txt
```

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
in the file `authors` where each line is a valid username. The provided
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

## Search

The final form of `main.py` should allow the user to invoke the script in a command line
and provide a search phrase as a first argument. The script should then return
a list of tweets that match the search phrase. The output format is up to you
and you should think about the usability of the output. A JSON output is useful
if you want to further process the output using another program but it may not
be the most readable if you just want to look at the tweets.

Here is an example of an interaction with the program, using an example of a
human readable output format.

```
$ python main.py "MySQL"
Number of matches: 1

Match nr. 1
Tweet by Josh Wills at 2022-02-18T22:54:16.000Z
Score: 6.0747194

@argyris @bernhardsson If you were choosing PlanetScale vs. MySQL for this, I
would pick RDS MySQL-- I &lt;3 Vitess/PlanetScale from Slack days, but 100%
MySQL compatibility is not really a thing given all of the quirks of MySQL.

If you were going to choose Postgres, then I think it's an interesting Q.
```

Elasticsearch provides a lot of ways of querying its contents.
[Here](https://www.elastic.co/guide/en/elasticsearch/reference/8.0/full-text-queries.html)
is the page for all the full-text search methods. For this exercise, you should
probably focus on these:

- [`match` query](https://www.elastic.co/guide/en/elasticsearch/reference/8.0/query-dsl-match-query.html)
- [`match_phrase` query](https://www.elastic.co/guide/en/elasticsearch/reference/8.0/query-dsl-match-query-phrase.html)

To help you create an effective command line interface in your script, you can
use the `argparse` module in the Python standard library.
[Here](https://docs.python.org/3.8/library/argparse.html) is the documentation
you will need.


## Bonus points

If you were able to get the functionality described above to work,
congratulations! You are awesome!

If you want to explore further, here are some ways you can improve on top of
what you have already built. These are provided in a rough order of difficulty.

- Provide an option for different output formats
- Insert a new tweet only if that tweet is not already present in the index
- Highlight the part of the tweet that matches the search phrase ([relevant documentation](https://www.elastic.co/guide/en/elasticsearch/reference/8.0/highlighting.html))
- Use a non-standard text analyzer ([relevant documentation](https://www.elastic.co/guide/en/elasticsearch/reference/8.0/analysis.html))

"""
This is a possible solution to the challenge proposed. It defines a command-line
interface with two subcommands:

    - insert: triggers the code to contact the Twitter API and insert the
    tweets in Elasticsearch
    - search: allows the user to search for a string in the corpus of tweets
    stored in Elasticsearch

The search subcommand has various option that allow the user to control the output
format, the type of match and if the matches should be highlighted or not.

There is also a help page that can be shown by running

> python main.py --help

This solution does not include the use of a non-standard text analyzer.
"""
import requests
import json
import configparser
from elasticsearch import Elasticsearch, helpers
import argparse

from pprint import pprint

MY_INDEX = 'twitter-gnog'

parser = argparse.ArgumentParser(
        description='Insert tweets in Elasticsearch and search them'
)

subparsers = parser.add_subparsers(dest='subcommand')

insert_parser = subparsers.add_parser('insert', help='Insert tweets into Elasticsearch')
search_parser = subparsers.add_parser('search', help='Search tweets in Elasticsearch')

search_parser.add_argument('query_string',
    help='The string to search for in the corpus of tweets'
)

search_parser.add_argument('--output-format', '-o',
    choices=['json', 'human'],
    default='human',
    help='The output format of the matches'
)

search_parser.add_argument('--highlight',
    action='store_true',
    help='Whether the matched words or phrases should be highlighted in the output'
)

search_parser.add_argument('--match_type', '-m',
    choices=['word', 'phrase'],
    default='word',
    help='Whether the search should be a simple word or phrase search'
)


config = configparser.RawConfigParser()
config.read('config.ini')

bearer_token = config['TWITTER']['bearer_token']

twitter_search_url = "https://api.twitter.com/2/tweets/search/recent"

es = Elasticsearch(
    cloud_id=config['ELASTIC']['cloud_id'],
    api_key=(config['ELASTIC']['apikey_id'], config['ELASTIC']['apikey_key']),
)

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def search_recent_tweets_by_user(twitter_user):
    query_params = {
            'query': '(from:{twitter_user} -is:retweet)'.format(twitter_user=twitter_user),
            'tweet.fields': {'created_at'},
            'expansions': 'author_id'
        }

    return connect_to_endpoint(twitter_search_url, query_params)

def process_api_response(json_response):
    """
    Takes a json response and processes it into a list of documents
    to be ingested into Elasticsearch.
    """

    # If no tweets were found for this user, return None
    if json_response['meta']['result_count'] == 0:
        return None

    author_name = json_response["includes"]["users"][0]["name"]
    author_username = json_response["includes"]["users"][0]["username"]

    result = []

    for tweet in json_response["data"]:
        tweet["author_name"] = author_name
        tweet["author_username"] = author_username

        result.append(tweet)

    return result

def insert_tweets():

    with open('authors', 'r') as f:
        authors_list = f.readlines()

    for author in authors_list:
        json_response = search_recent_tweets_by_user(author)
        tweets = process_api_response(json_response)
        if tweets:
            for tweet in tweets:
                es.index(index=MY_INDEX, document=tweet, id=tweet['id'])

def search_tweets(query_string, output_format, highlight, match_type):

    if match_type == 'word':
        query_body = {'match': {'text': query_string}}
    else:
        query_body = {'match_phrase': {'text': query_string}}

    if highlight:
        highlight_body = {'fields': {'text': {}}}
    else:
        highlight_body = None

    search_results = es.search(index=MY_INDEX, query=query_body, highlight=highlight_body)

    if output_format == 'json':
        for hit in search_results['hits']['hits']:
            print(json.dumps(hit))
    elif output_format == 'human':
        print('Number of matches:', search_results['hits']['total']['value'])
        print('')
        for i, hit in enumerate(search_results['hits']['hits']):
            print('Match nr.', i+1)
            print('Tweet by {author} at {timestamp}'.format(
                author=hit['_source']['author_name'],
                timestamp=hit['_source']['created_at']
                )
            )
            print('Score:', hit['_score'])
            print('')
            if highlight:
                for highlighted_text in hit['highlight']['text']:
                    print(highlighted_text)
            else:
                print(hit['_source']['text'])
            print('')

def main():
    args = parser.parse_args()
    if args.subcommand == 'insert':
        insert_tweets()
    elif args.subcommand == 'search':
        search_tweets(args.query_string, args.output_format, args.highlight, args.match_type)
    else:
        # Not a valid invocation of the script
        # Print some help to the user
        parser.print_usage()

if __name__ == "__main__":
    main()

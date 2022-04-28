import requests
import json
import configparser
from elasticsearch import Elasticsearch, helpers

from pprint import pprint

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

def main():

    with open('authors', 'r') as f:
        authors_list = f.readlines()

    for author in authors_list:
        json_response = search_recent_tweets_by_user(author)
        tweets = process_api_response(json_response)
        if tweets:
            for tweet in tweets:
                es.index(index='twitter-gnog', document=tweet, id=tweet['id'])

if __name__ == "__main__":
    main()

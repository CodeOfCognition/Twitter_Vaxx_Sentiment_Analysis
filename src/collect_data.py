import json
import requests
import os
from dotenv import load_dotenv
import argparse
from datetime import timedelta, datetime
import tweepy

# Load authentication keys into environment
load_dotenv()

def parse_args():

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='<query_file.txt>', required=True)
    parser.add_argument('-o', help='<output.json>', required=True)
    parser.add_argument('-n', help='<sample size>', default=5000)
    parser.add_argument('-since_id', help='id of last tweet', default=None)
    args = parser.parse_args()

    return args.i, args.o, int(args.n), args.since_id

def get_api():
    auth = tweepy.AppAuthHandler(os.getenv('API_KEY'), os.getenv('API_SECRET'))
    api = tweepy.API(auth, wait_on_rate_limit=True)

    return api

def get_query(input_fname):
    
    with open(input_fname, 'r') as f:
        query = f.read().rstrip('\n')
    
    return query


def get_sample(api, query, sample_size, since_id=None):
    
    tweets = {}
    newest = None
    newest_id = None
    for tweet in tweepy.Cursor(api.search_tweets, query, since_id=since_id, count=100).items(sample_size):
        if tweet.id not in tweets:
            tweets[tweet.id_str] = {}
            tweets[tweet.id_str]['text'] = tweet.text
            tweets[tweet.id_str]['retweet_count'] = tweet.retweet_count
            tweets[tweet.id_str]['favorite_count'] = tweet.favorite_count
            
            if newest == None:
                newest = tweet.created_at
                newest_id = tweet.id
            elif tweet.created_at > newest:
                newest = tweet.created_at
                newest_id = tweet.id
    
    return tweets, newest_id


def main():

    input_fname, output_fname, sample_size, since_id = parse_args()
    
    query = get_query(input_fname)
    
    api = get_api()
    
    sample, newest_id = get_sample(api, query, sample_size, since_id)
   
    print(f'The id of the latest tweet in our dataset is: {newest_id}')

    with open(output_fname, 'w') as f:
        json.dump(sample, f, indent=2)

if __name__=='__main__':
    main()

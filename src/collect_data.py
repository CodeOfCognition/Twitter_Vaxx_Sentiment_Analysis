import json
import requests
import os
from dotenv import load_dotenv
import argparse
from datetime import timedelta, datetime
import tweepy

def parse_args():

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='<query_file.txt>', required=True)
    parser.add_argument('-o', help='<output.json>', required=True)
    parser.add_argument('-n', help='<sample size>', default=1000)
    parser.add_argument('-since_id', help='id of last tweet', default=None)
    parser.add_argument('-max_id', help='<get tweets older than ID>', default=None)
    parser.add_argument('-end_time', help='get tweets before provided date: YYYY-MM-DDTHH:mm:ssZ', default=None)
    parser.add_argument('-start_time', help='Earliest time from which to search tweets:YYYY-MM-DDTHH:mm:ssZ', default=None)
    args = parser.parse_args()

    return args.i, args.o, int(args.n), args.since_id, args.max_id, args.end_time, args.start_time


def get_client():
    # Authenticate using env keys and initialize API object
    #auth = tweepy.AppAuthHandler(os.getenv('API_KEY'), os.getenv('API_SECRET'))
    api_client = tweepy.Client(os.getenv('BEARER_TOKEN'),os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'),
                               os.getenv('API_KEY'), os.getenv('API_SECRET'), return_type=requests.Response, wait_on_rate_limit=True)

    return api_client


def get_query(input_fname):
    # Load query from file    
    with open(input_fname, 'r') as f:
        query = f.read().rstrip('\n')

    return query


def search_tweets(api_client, query, sample_size, since_id, until_id, end_time, start_time):
    responses = []
    next_token = None
    tweet_fields = ['public_metrics', 'created_at']
    oldest_id = None
    newest_id = None
    
    if sample_size < 100:
        max_results = sample_size
    else:
        max_results = 100

    while sample_size > 0:
        re = api_client.search_recent_tweets(query, end_time=end_time, max_results=max_results, next_token=next_token, since_id=since_id, tweet_fields=tweet_fields,
                                             until_id=until_id, start_time=start_time)
        json_re = re.json()
        next_token = json_re['meta']['next_token']
        sample_size -= json_re['meta']['result_count']

        if newest_id == None:
            newest_id = json_re['meta']['newest_id']
        elif json_re['meta']['newest_id'] > newest_id:
            newest_id = json_re['meta']['newest_id']

        if oldest_id == None:
            oldest_id = json_re['meta']['oldest_id']
        elif json_re['meta']['oldest_id'] < oldest_id:
            oldest_id = json_re['meta']['oldest_id']
        
        responses.append(json_re)

    return responses, oldest_id, newest_id 

def get_json(responses):

    json_dict = {'data':[]}

    for re in responses:
        json_dict['data'] += re['data']

    return json_dict

def collect_data(input_fname, output_fname, sample_size, since_id=None, max_id=None, end_time=None, start_time=None):
    # Function for running as import
    
    # Load authentication keys into environment
    load_dotenv()    
    
    query = get_query(input_fname)

    api_client = get_client()

    responses, oldest_id, newest_id = search_tweets(api_client, query, sample_size, since_id, max_id, end_time, start_time)

    json_dict = get_json(responses)

    with open(output_fname, 'w') as f:
        json.dump(json_dict, f, indent=2)
    
    return oldest_id, newest_id

def main():
    # Load authentication keys into environment
    load_dotenv()
    
    input_fname, output_fname, sample_size, since_id, max_id, end_time, start_time = parse_args()
    
    query = get_query(input_fname)
    
    api_client = get_client()
    
    responses, oldest_id, newest_id = search_tweets(api_client, query, sample_size, since_id, max_id, end_time, start_time)
   
    json_dict = get_json(responses)

    with open(output_fname, 'w') as f:
        json.dump(json_dict, f, indent=2)
    
    return oldest_id, newest_id 

if __name__=='__main__':
    main()

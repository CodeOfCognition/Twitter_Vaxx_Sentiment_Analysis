import json
import tweepy
import argparse
from dotenv import load_dotenv
import os

def parse_args():

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='<id_file>', default=None)
    parser.add_argument('-id', help='<single tweet ID>', default=None)
    parser.add_argument('-o', help='<output.json>', default=None)
    args = parser.parse_args()

    return args.i, args.id, args.o


def get_api():
    # Authenticate using env keys and initialize API object
    auth = tweepy.AppAuthHandler(os.getenv('API_KEY'), os.getenv('API_SECRET'))
    api = tweepy.API(auth, wait_on_rate_limit=True)

    return api

def get_id_list(id_fname):

    id_list = []

    with open(id_fname, 'r') as f:
        id_list.append(f.read().lstrip('\n'))

    return id_list


def lookup_tweet(api, tweet_id):
    
    tweet_dict = {}

    for tweet in api.lookup_statuses(tweet_id):
        tweet_dict[tweet.id] = {}
        dtlocal = tweet.created_at.astimezone()
        tweet_dict[tweet.id]['created_at'] = dtlocal.strftime('%d/%m/%y %I:%M %S %p')
    
    return tweet_dict

    
def main():
    # Authentication keys from .env file
    load_dotenv()
    
    id_fname, single_id, output = parse_args()
    
    api = get_api()

    if id_fname is not None:
        id_list = get_id_list(id_fname)
        tweet_dict = lookup_tweet(api, id_list)
    elif single_id is not None:
        tweet_dict = lookup_tweet(api, [single_id])
    else:
        print('USAGE ERROR: must provide filename with tweet ids XOR single tweet ID')
        quit()

    if output is None:
        print(json.dumps(tweet_dict, indent=3))
    else:
        with open(output, 'w') as f:
            json.dumps(tweet_dict, f, indent=3)

if __name__=='__main__':
    main()

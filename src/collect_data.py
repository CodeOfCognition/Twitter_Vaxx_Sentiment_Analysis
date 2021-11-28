import json
import requests
import os
from dotenv import load_dotenv
import argparse
# Load authentication keys into environment
load_dotenv()

base_url = 'https://api.twitter.com/'

def parse_args():

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='<query_file.txt>', required=True)
    parser.add_argument('-o', help='<output.json>', required=True)
    args = parser.parse_args()

    return args.i, args.o

def authenticate():
    # Create authentication token
    auth = requests.auth.HTTPBasicAuth(os.getenv('API_KEY'), os.getenv('API_SECRET'))

    # Create login type dictionary with login credentials
    data = {
        'grant_type': 'client_credentials',
    }

    # Create user-agent in headers
    headers = {'User-Agent':'vaxx-sentiment/0.0.1'}

    # Request access token from reddit api
    res = requests.post(f'{base_url}oauth2/token', auth=auth,
                        data=data, headers=headers)

    # Get the token
    TOKEN = res.json()['access_token']

    # Add authorization to headers
    headers['Authorization'] = f'bearer {TOKEN}'

    return headers

def get_query(input_fname):
    
    with open(input_fname, 'r') as f:
        query = f.read()

    return query

def get_sample(headers, query):
    
    re = requests.get(f'{base_url}2/tweets/search/recent', headers=headers, params={'query':query, 'max_results':'100'})

    return re.json()

def main():

    input_fname, output_fname = parse_args()
    
    query = get_query(input_fname)

    headers = authenticate()
        
    sample = get_sample(headers, query)
    
    with open(output_fname, 'w') as f:
        json.dump(sample, f, indent=3)

if __name__=='__main__':
    main()

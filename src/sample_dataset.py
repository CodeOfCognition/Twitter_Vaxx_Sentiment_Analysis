import os
import argparse
from datetime import datetime as dt
from datetime import timedelta
from dateutil.parser import isoparse
import json
import collect_data as cd 
import lookup_tweet as look

def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('-start', help='Datetime from which to start', required=True)
    parser.add_argument('-periods', help='Number of periods of length 1h to sample', required=True)
    parser.add_argument('-query', help='Text file containing query', required=True)
    parser.add_argument('-n_tweets', help='Number of tweets to sample at each period', required=True)
    parser.add_argument('-save_dir', required=True)
    args = parser.parse_args()

    return args.start, int(args.periods), args.query, int(args.n_tweets), args.save_dir


def main():
    start, num_periods, query, num_tweets, save_dir = parse_args()
    
    sample_time = isoparse(start)
    delta = timedelta(hours=1) 
    now = dt.now().astimezone()
    
    runs = {}

    for p in range(num_periods):
        if sample_time > now:
            break
        save_path = os.path.join(save_dir, f'tweets{p+95}.json')
        start_time = sample_time.strftime('%Y-%m-%dT%H:%M:%S%z')
        
        _, newest = cd.collect_data(query, save_path, num_tweets, end_time=sample_time)   
        
        sample_time += delta

if __name__=='__main__':
    main()

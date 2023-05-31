"""
Hydrate tweets from a dataframe with tweet_id
"""


# ------------------------------------------- IMPORTS -------------------------------------------

# General imports
import os
import pandas as pd
import csv
from tqdm import tqdm
import argparse
from twarc import Twarc2

# Local imports
from utils import get_metadata
from env import get_consumer_key, get_consumer_secret, get_access_token, get_access_token_secret


# ------------------------------------------- SCRIPT -------------------------------------------

def main():
    df = pd.read_csv(file)

    print(f'Getting data with {len(df)} tweets')

    csv_file = open(f'{file.split(".")[0]}_hydrated.csv', 'w+', encoding='utf-8')
    csv_writer = csv.writer(csv_file)

    csv_writer.writerow(['tweet_id', 'user_id', 'timestamp', 'text', 'lang', 'class'])

    iter = 0
    for batchs in tqdm(range(0, len(df), 100)):
        for tweet in get_metadata(df['tweet_id'].tolist()[batchs:batchs + 100], t):
            csv_writer.writerow(
                [tweet['id'], tweet['author_id'], tweet['created_at'], tweet['text'].replace('\n', ''),
                 tweet['lang'],
                 class_])
            iter += 1

    csv_file.close()
    print(f'Got {iter} tweets\n'
          f'------------------------------------------')


# ------------------------------------------- MAIN -------------------------------------------

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hydrate tweets from a csv file with tweet_id')

    parser.add_argument('--file', type=str, help='File with tweet_id to hydrate', required=True)
    parser.add_argument('--env', type=str, help='Environment file to get twitter credentials, '
                                                'consumer_key, consumer_secret, access_token, access_token_secret',
                        required=True)
    parser.add_argument('--class_', type=str, default='1', help='Class of the tweets (Default: 1)')

    args = parser.parse_args()
    class_ = args.class_
    file = args.file

    # Set up twarc
    consumer_key = get_consumer_key(args.env)
    consumer_secret = get_consumer_secret(args.env)
    acces_token = get_access_token(args.env)
    acces_token_secret = get_access_token_secret(args.env)
    t = Twarc2(consumer_key, consumer_secret, acces_token, acces_token_secret)

    main()

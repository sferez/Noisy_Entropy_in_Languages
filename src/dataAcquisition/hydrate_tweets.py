"""
:author: Siméon FEREZ
:version: 1.0.0
:copyright: Copyright © 2023 by Siméon FEREZ. All rights reserved. This work may not be reproduced, in whole or in part, without the written permission of the author.
:description: Hydrate tweets from a csv file with tweet_id

CLI Arguments:
    - --input, --i: Directory or CSV file
    - --env: Environment file to get twitter credentials, consumer_key, consumer_secret, access_token, access_token_secret

Example:
    >>> python hydrate_tweets.py --input data.csv --env .env
"""

# ------------------------------------------- IMPORTS -------------------------------------------

# External
import os
import pandas as pd
import csv
from tqdm import tqdm
import argparse
from twarc import Twarc2
from pathlib import Path

# Internal
from utils import get_metadata
from env import get_consumer_key, get_consumer_secret, get_access_token, get_access_token_secret


# ------------------------------------------- FUNCTIONS -------------------------------------------

def process_file(fp):
    """
    Process a csv file with tweet_id and hydrate it

    :param fp: File path
    :type fp: str
    :return: None
    :rtype: None

    >>> process_file('data.csv')
    """
    df = pd.read_csv(fp)
    tweet_id_df = df[['tweet_id']].dropna().astype(int)

    print(f'Hydrating {fp}')

    csv_file = open(os.path.join(Path(fp).name, '_hydrated'), 'w+', encoding='utf-8')
    csv_writer = csv.writer(csv_file)

    csv_writer.writerow(['tweet_id', 'user_id', 'timestamp', 'text', 'lang'])

    iter = 0
    for batchs in tqdm(range(0, len(tweet_id_df), 100)):
        for tweet in get_metadata(tweet_id_df['tweet_id'].tolist()[batchs:batchs + 100], t):
            csv_writer.writerow(
                [tweet['id'], tweet['author_id'], tweet['created_at'], tweet['text'].replace('\n', ''),
                 tweet['lang']])
            iter += 1

    csv_file.close()
    print(f'Got {iter} tweets\n'
          f'------------------------------------------')


# ------------------------------------------- SCRIPT -------------------------------------------

def main():
    """
    Main function of hydrate_tweets.py

    :return: None
    :rtype: None

    >>> main()
    """
    if os.path.isfile(input_):
        fp = input_
        process_file(fp)
    else:
        for root, dirs, files in os.walk(input_):
            for file in files:
                if file.endswith(".csv"):
                    print(file)
                    fp = os.path.join(root, file)
                    process_file(fp)


# ------------------------------------------- MAIN -------------------------------------------

if __name__ == '__main__':
    """
    Command line arguments of hydrate_tweets.py
    
    Args:
        --input, --i: Directory or CSV file
        --env: Environment file to get twitter credentials, consumer_key, consumer_secret, access_token, access_token_secret
        
    Example:
        >>> python hydrate_tweets.py --input data.csv --env .env
    """
    parser = argparse.ArgumentParser(description='Hydrate tweets from a csv file with tweet_id')

    parser.add_argument('--input', '--i', type=str, help='Directory or CSV file', required=True)
    parser.add_argument('--env', type=str, help='Environment file to get twitter credentials, '
                                                'consumer_key, consumer_secret, access_token, access_token_secret',
                        required=True)

    args = parser.parse_args()
    input_ = args.input

    # Set up twarc
    consumer_key = get_consumer_key(args.env)
    consumer_secret = get_consumer_secret(args.env)
    acces_token = get_access_token(args.env)
    acces_token_secret = get_access_token_secret(args.env)
    t = Twarc2(consumer_key, consumer_secret, acces_token, acces_token_secret)

    main()

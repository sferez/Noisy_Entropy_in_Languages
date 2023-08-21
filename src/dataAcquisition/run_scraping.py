"""
:author: Siméon FEREZ
:version: 1.0.0
:copyright: Copyright © 2023 by Siméon FEREZ. All rights reserved. This work may not be reproduced, in whole or in part, without the written permission of the author.
:description: Scraping Twitter with Seleniu and create a csv file with the data.

CLI Arguments:
    - --start, --s: Start date
    - --end, --e: End date (default: today)
    - --interval, --i: Interval (default: 1)
    - --env: Environment file with Chrome driver path and Twitter credentials
    - --from_account, --a: From account
    - --hashtag, --h: Hashtag to search
    - --word, --w: Word to search
    - --headless: Headless mode (default: False)
    - --only_id: Only collect tweet_id (default: False)

Examples:
    >>>python3 run_scraping.py --start 2021-01-01 --end 2021-01-31 --env scraping.env --from_account elonmusk
    >>>python3 run_scraping.py --start 2021-01-01 --end 2021-01-31 --env scraping.env --hashtag bitcoin
    >>>python3 run_scraping.py --start 2021-01-01 --end 2021-01-31 --env scraping.env --word ukraine
"""

# ---------------------------------------------------- IMPORTS ------------------------------------------------------- #

# External
import argparse
from datetime import datetime
import time
import sys

# Internal
from scraping import scraping
from utils import init_driver


# ---------------------------------------------------- SCRIPT -------------------------------------------------------- #

def main():
    """
    Main function of run_scraping.py

    :return: None
    :rtype: None

    >>> main()
    """
    print(f'Scraping from {start} to {end}')
    driver = init_driver(headless=headless, show_images=False, env=env)
    if mode == 'account':
        print(f'Searching tweets from {from_account}...')
        data = scraping(start, until=end, interval=interval, from_account=from_account,
                        save_dir=f"../../data/scraping/{from_account}", driver=driver, env=env, headless=headless,
                        only_id=only_id, resume=True)
    elif mode == 'hashtag':
        print(f'Searching tweets with hashtag {hashtag}...')
        data = scraping(start, until=end, interval=interval, hashtag=hashtag,
                        save_dir=f"../../data/scraping/{hashtag}", driver=driver, env=env, headless=headless,
                        only_id=only_id, resume=True)
    elif mode == 'word':
        print(f'Searching tweets with word {word}...')
        data = scraping(start, until=end, interval=interval, words=word,
                        save_dir=f"../../data/scraping/{word}", driver=driver, env=env, headless=headless,
                        only_id=only_id, resume=True)

    print(f'Scraping finished, {len(data)} tweets scraped from {start} to {end}')
    sys.exit(0)


# ---------------------------------------------------- MAIN ---------------------------------------------------------- #


if __name__ == "__main__":
    """
    Command line arguments of run_scraping.py
    
    Args:
        --start, --s: Start date
        --end, --e: End date (default: today)
        --interval, --i: Interval (default: 1)
        --env: Environment file with Chrome driver path and Twitter credentials
        --from_account, --a: From account
        --hashtag, --h: Hashtag to search
        --word, --w: Word to search
        --headless: Headless mode (default: False)
        --only_id: Only collect tweet_id (default: False)
        
    Examples:
        >>>python3 run_scraping.py --start 2021-01-01 --end 2021-01-31 --env scraping.env --from_account elonmusk
        >>>python3 run_scraping.py --start 2021-01-01 --end 2021-01-31 --env scraping.env --hashtag bitcoin
        >>>python3 run_scraping.py --start 2021-01-01 --end 2021-01-31 --env scraping.env --word ukraine
    """
    parser = argparse.ArgumentParser(description='Scraping Twitter')

    parser.add_argument('--start', '--s', type=str, help='Start date', required=True)
    parser.add_argument('--end', '--e', type=str, help='End date', default=datetime.now().strftime("%Y-%m-%d"))
    parser.add_argument('--interval', '--i', type=int, help='Interval', default=1)
    parser.add_argument('--env', type=str, help='Environment file with Chrome driver path and Twitter credentials',
                        required=True)
    parser.add_argument('--from_account', '--a', type=str, help='From account')
    parser.add_argument('--hashtag', '--h', type=str, help='Hashtag to search')
    parser.add_argument('--word', '--w', type=str, help='Word to search')
    parser.add_argument('--headless', action=argparse.BooleanOptionalAction, help='Headless mode', default=False)
    parser.add_argument('--only_id', action=argparse.BooleanOptionalAction, help='Only collect tweet_id', default=False)

    args = parser.parse_args()

    env = args.env
    start = args.start
    end = args.end
    interval = int(args.interval)
    headless = args.headless
    only_id = args.only_id

    if '--from_account' or '--a' in sys.argv:
        from_account = args.from_account
        mode = 'account'
    elif '--hashtag' or '--h' in sys.argv:
        hashtag = args.hashtag
        mode = 'hashtag'
    elif '--word' or '--w' in sys.argv:
        word = args.word
        mode = 'word'
    else:
        raise ValueError('You must specify an account, hashtag or word to search. Use --from_account, --hashtag or --word')

    timeout = 0
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("\nReceived interrupt, stopping...")
            sys.exit(0)
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            timeout += 1
            print(f'\nTimeout: {timeout}, restarting stream...')
            # Add a delay before retrying
            time.sleep(60)  # adjust this value according to your needs

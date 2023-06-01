"""
Script to run scraping.py with arguments from command line.

Personalities (Class 1):
    @elonmusk start: 2010-01-01 X
    @billgates start: 2009-01-01
    @barackobama start: 2007-01-01 X
    @emmanuelmacron start: 2013-01-01 X
    @sanchezcastejon start: 2009-01-01

News (Class 2):
    # English
    @BBCNews start: 2007-01-01 ~
    @CNN start: 2007-01-01 ~
    @nytimes start: 2007-01-01 X
    @guardian start: 2007-01-01 ~
    @Reuters start: 2007-01-01 ~

    # French
    1. Le Monde (@lemondefr) ~
    2. Le Figaro (@Le_Figaro)
    3. Libération (@libe)
    4. France 24 (@FRANCE24)
    5. L'Express (@LEXPRESS)

    # Spanish
    1. El País (@el_pais)
    2. El Mundo (@elmundoes)
    3. La Vanguardia (@LaVanguardia)
    4. ABC.es (@abc_es)
    5. El Confidencial (@elconfidencial)
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
    print(f'Scraping from {start} to {end} for {from_account}')
    driver = init_driver(headless=headless, show_images=False, env=env)
    data = scraping(start, until=end, interval=1, from_account=from_account,
                    save_dir=f"../../data/scraping/{from_account}", driver=driver, env=env, headless=headless,
                    only_id=only_id, Class=class_, resume=True)
    print(f'Scraping finished for {from_account}, {len(data)} tweets scraped from {start} to {end}')
    sys.exit(0)

# ---------------------------------------------------- MAIN ---------------------------------------------------------- #


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scraping Twitter')

    parser.add_argument('--start', type=str, help='Start date', required=True)
    parser.add_argument('--end', type=str, help='End date', default=datetime.now().strftime("%Y-%m-%d"))
    parser.add_argument('--interval', type=int, help='Interval', default=1)
    parser.add_argument('--from_account', type=str, help='From account', required=True)
    parser.add_argument('--env', type=str, help='Environment file with Chrome driver path and Twitter credentials',
                        required=True)
    parser.add_argument('--headless', action=argparse.BooleanOptionalAction, help='Headless mode', default=False)
    parser.add_argument('--class_', type=str, help='Class', default='1')
    parser.add_argument('--only_id', action=argparse.BooleanOptionalAction, help='Only collect tweet_id', default=False)

    args = parser.parse_args()

    env = args.env
    start = args.start
    end = args.end
    interval = args.interval
    from_account = args.from_account
    headless = args.headless
    class_ = args.class_
    only_id = args.only_id

    args = parser.parse_args()

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

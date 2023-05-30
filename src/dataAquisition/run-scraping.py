"""
Script to run scraping.py with arguments from command line.

Personalities (Class 1):
    @elonmusk start: 2010-01-01
    @billgates start: 2009-01-01
    @barackobama start: 2007-01-01
    @emmanuelmacron start: 2013-01-01
    @sanchezcastejon start: 2009-01-01

News (Class 2):
    # English
    @BBCNews start: 2007-01-01
    @CNN start: 2007-01-01
    @nytimes start: 2007-01-01
    @guardian start: 2007-01-01
    @Reuters start: 2007-01-01

    # French
    @lemondefr start: 2007-01-01
    @lefigaro start: 2007-01-01
    @le_Parisien start: 2007-01-01
    @20Minutes start: 2007-01-01
    @BFMTV start: 2007-01-01

    # Spanish
    @elmundoes start: 2007-01-01
    @el_pais start: 2007-01-01
    @abc_es start: 2007-01-01
    @LaVanguardia start: 2007-01-01
    @EFEnoticias start: 2007-01-01
"""

# ---------------------------------------------------- IMPORTS ------------------------------------------------------- #

# External
import argparse
from datetime import datetime

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

    driver.close()
    driver.quit()


# ---------------------------------------------------- MAIN ---------------------------------------------------------- #


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scraping Twitter')

    parser.add_argument('--start', type=str, help='Start date', required=True)
    parser.add_argument('--end', type=str, help='End date', required=True, default=datetime.now().strftime("%Y-%m-%d"))
    parser.add_argument('--interval', type=int, help='Interval', default=1)
    parser.add_argument('--from_account', type=str, help='From account', required=True)
    parser.add_argument('--env', type=str, help='Environment file with Chrome driver path and Twitter credentials',
                        required=True)
    parser.add_argument('--headless', type=bool, help='Headless', default=True)
    parser.add_argument('--class_', type=str, help='Class', default='1')
    parser.add_argument('--only_id', type=bool, help='Save only the tweet_id', default=False)

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

    main()

"""
:author: Siméon FEREZ
:version: 1.0.0
:copyright: Copyright © 2023 by Siméon FEREZ. All rights reserved. This work may not be reproduced, in whole or in part, without the written permission of the author.
:credits: Scweet: An extensive toolbox to scrape Twitter, written in Python.
:description: Twitter scraping module.
"""

# -------------------------------------------- IMPORTS --------------------------------------------------------------- #

# External
import csv
import os
import datetime
from time import sleep
import random
import pandas as pd
import subprocess

# Internal
from utils import get_last_date_from_csv, log_search_page, keep_scroling, log_in


# -------------------------------------------- FUNCTIONS ------------------------------------------------------------- #


def scraping(since, until=None, words=None, to_account=None, from_account=None, mention_account=None, interval=5,
             lang=None,
             headless=True, limit=float("inf"), display_type="Top", resume=False, proxy=None, hashtag=None,
             save_dir="outputs", filter_replies=False, proximity=False,
             geocode=None, minreplies=None, minlikes=None, minretweets=None, driver=None, env=None, only_id=False):
    """
    :Function: Scraping tweets from Twitter.

    :param since: date from which we start scraping
    :type since: str
    :param until: date until which we scrape
    :type until: str
    :param words: list of words to search for
    :type words: list
    :param to_account: account to which we search for tweets
    :type to_account: str
    :param from_account: account from which we search for tweets
    :type from_account: str
    :param mention_account: account to which we search for tweets
    :type mention_account: str
    :param interval: interval of time between two searches
    :type interval: int
    :param lang: language of the tweets
    :type lang: str
    :param headless: headless mode
    :type headless: bool
    :param limit: limit of tweets to scrape
    :type limit: int
    :param display_type: type of display
    :type display_type: str
    :param resume: resume scraping from previous work
    :type resume: bool
    :param proxy: proxy to use
    :type proxy: str
    :param hashtag: hashtag to search for
    :type hashtag: str
    :param save_dir: directory to save the scraped tweets
    :type save_dir: str
    :param filter_replies: filter replies
    :type filter_replies: bool
    :param proximity: proximity search
    :type proximity: bool
    :param geocode: geocode
    :type geocode: str
    :param minreplies: minimum number of replies
    :type minreplies: int
    :param minlikes: minimum number of likes
    :type minlikes: int
    :param minretweets: minimum number of retweets
    :type minretweets: int
    :param driver: driver to use
    :type driver: selenium.webdriver
    :param env: environment to use
    :type env: str
    :param only_id: only scrape tweet ids
    :type only_id: bool
    :return: scraped tweets
    :rtype: pd.DataFrame

    >>> scraping(since='2020-01-01', until='2020-01-02', words=['covid', 'corona'], interval=1, save_dir='outputs')
    >>> scraping(since='2020-01-01', until='2020-01-02', to_account='@elonmusk', interval=1, save_dir='outputs')
    """
    # ------------------------- Variables :
    # header of csv
    if only_id:
        header = ['tweet_id']
    else:
        header = ['tweet_id', "user_id", 'timestamp', 'text']
    # list that contains all data
    data = []
    # unique tweet ids
    tweet_ids = set()
    # write mode
    write_mode = 'w'
    # start scraping from <since> until <until>
    # add the <interval> to <since> to get <until_local> for the first refresh
    # if <until>=None, set it to the actual date
    if until is None:
        until = datetime.date.today().strftime("%Y-%m-%d")
    # set refresh at 0. we refresh the page for each <interval> of time.
    refresh = 0

    # ------------------------- settings :
    # file path
    if words:
        if type(words) == str:
            words = words.split("//")
        path = save_dir + "/" + '_'.join(words) + '_' + str(since).split(' ')[0] + '_' + \
               str(until).split(' ')[0] + '.csv'
    elif from_account:
        path = save_dir + "/" + from_account + '_' + str(since).split(' ')[0] + '_' + str(until).split(' ')[
            0] + '.csv'
    elif to_account:
        path = save_dir + "/" + to_account + '_' + str(since).split(' ')[0] + '_' + str(until).split(' ')[
            0] + '.csv'
    elif mention_account:
        path = save_dir + "/" + mention_account + '_' + str(since).split(' ')[0] + '_' + str(until).split(' ')[
            0] + '.csv'
    elif hashtag:
        path = save_dir + "/" + hashtag + '_' + str(since).split(' ')[0] + '_' + str(until).split(' ')[
            0] + '.csv'
    # create the <save_dir>
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # init the driver
    t = 0
    while t < 5:
        try:
            log_in(driver, env, wait=10)
            break
        except:
            print(f'Error while logging in. Retrying... ({t + 1}/5)')
            sleep(2)
            t += 1
            if t == 5:
                print('Failed to log in. Exiting...')
                raise Exception('Failed to log in.')
            continue

    # resume scraping from previous work
    if os.path.exists(path) and resume and not only_id:
        if int(subprocess.check_output(f"wc -l {path}", shell=True).split()[0]) - 1 > 0:
            since = str(get_last_date_from_csv(path))[:10]
            write_mode = 'a'
            print(f'Resuming scraping from {since}...')
    until_local = datetime.datetime.strptime(since, '%Y-%m-%d') + datetime.timedelta(days=interval)

    # start scraping
    with open(path, write_mode, newline='', encoding='utf-8') as f:
        writer = csv.writer(f, escapechar='\\')
        if write_mode == 'w':
            writer.writerow(header)

        # log search page for a specific <interval> of time and keep scrolling unltil scrolling stops or reach the <until>
        while until_local <= datetime.datetime.strptime(until, '%Y-%m-%d'):
            # number of scrolls
            sleep(random.uniform(1, 3))
            scroll = 0
            # convert <since> and <until_local> to str
            if type(since) != str:
                since = datetime.datetime.strftime(since, '%Y-%m-%d')
            if type(until_local) != str:
                until_local = datetime.datetime.strftime(until_local, '%Y-%m-%d')
            # log search page between <since> and <until_local>
            path = log_search_page(driver=driver, words=words, since=since,
                                   until_local=until_local, to_account=to_account,
                                   from_account=from_account, mention_account=mention_account, hashtag=hashtag,
                                   lang=lang,
                                   display_type=display_type, filter_replies=filter_replies, proximity=proximity,
                                   geocode=geocode, minreplies=minreplies, minlikes=minlikes, minretweets=minretweets)
            # number of logged pages (refresh each <interval>)
            refresh += 1
            # number of days crossed
            # days_passed = refresh * interval
            # last position of the page : the purpose for this is to know if we reached the end of the page or not so
            # that we refresh for another <since> and <until_local>
            last_position = driver.execute_script("return window.pageYOffset;")
            # should we keep scrolling ?
            scrolling = True
            print("looking for tweets between " + str(since) + " and " + str(until_local) + " ...")
            # number of tweets parsed
            tweet_parsed = 0
            # sleep 
            sleep(random.uniform(0.5, 1.5))
            # start scrolling and get tweets
            driver, data, writer, tweet_ids, scrolling, tweet_parsed, scroll, last_position = \
                keep_scroling(driver, data, writer, tweet_ids, scrolling, tweet_parsed, limit, scroll, last_position,
                              only_id=only_id)

            # keep updating <start date> and <end date> for every search
            if type(since) == str:
                since = datetime.datetime.strptime(since, '%Y-%m-%d') + datetime.timedelta(days=interval)
            else:
                since = since + datetime.timedelta(days=interval)
            if type(since) != str:
                until_local = datetime.datetime.strptime(until_local, '%Y-%m-%d') + datetime.timedelta(days=interval)
            else:
                until_local = until_local + datetime.timedelta(days=interval)

            print(f'Nb of Tweets : {tweet_parsed}')

    if only_id:
        data = pd.DataFrame(data, columns=['tweet_id'])
    else:
        data = pd.DataFrame(data, columns=['tweet_id', "user_id", 'timestamp', 'text'])

    # close the web driver
    driver.close()

    return data

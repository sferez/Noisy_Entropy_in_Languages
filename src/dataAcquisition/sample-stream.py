"""
Script to get a sample of the Twitter stream, using the Twitter API v2.
Gather 1% of the real-time stream of Tweets based on a sample of all Tweets.
Filter by language and save the data in a csv file.
"""

# ------------------------------------------- IMPORTS ----------------------------------------------------- #

# External
import requests
import os
import json
import csv
import datetime
import sys
import argparse
import time

# Internal
from env import get_bearer_token


# ------------------------------------------- FUNCTIONS ------------------------------------------------------ #

def create_url():
    # Add the parameters you want to the URL
    tweet_fields = "tweet.fields=lang,created_at,geo"
    expansions = "expansions=author_id,geo.place_id"
    # user_fields = "user.fields=location"
    place_fields = "place.fields=country_code,geo,id"
    url = f"https://api.twitter.com/2/tweets/sample/stream?{tweet_fields}&{expansions}&{place_fields}"
    return url


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2SampledStreamPython"
    return r


def check_date():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    global date, csv_file, csv_writer, iter_
    if current_date != date:
        csv_file.close()
        date = current_date
        filename = '../../data/sample-stream/' + date + '.csv'
        csv_file = open(filename, 'a+', encoding='utf-8')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['tweet_id', 'user_id', 'timestamp', 'text', 'lang'])
        iter_ = {l: 0 for l in languages}
        print(f'New date: {date}, reseting iter_')


def connect_to_endpoint(url):
    global iter_
    response = requests.request("GET", url, auth=bearer_oauth, stream=True)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            # if lang not in languages skip
            lang = json_response['data']['lang'] if 'lang' in json_response['data'] else None
            if lang not in languages:
                continue
            if iter_[lang] >= iter_max:
                if all([iter_[l] >= iter_max for l in iter_]):
                    csv_file.close()
                    exit()
                continue
            # Extract the fields you want from the response
            tweet_id = json_response['data']['id']
            author_id = json_response['data']['author_id']
            timestamp = json_response['data']['created_at']
            text = json_response['data']['text']
            text = text.replace('\n', ' ')
            check_date()
            csv_writer.writerow([tweet_id, author_id, timestamp, text, lang])
            iter_[lang] += 1
            sys.stdout.write('\r')
            msg = f'{" ".join([f"{l}: {iter_[l]}" for l in iter_])}'
            sys.stdout.write(msg)


# ------------------------------------------- MAIN ----------------------------------------------------------- #

def main():
    url = create_url()
    timeout = 0
    while True:
        try:
            connect_to_endpoint(url)
        except KeyboardInterrupt:
            print("\nReceived interrupt, stopping...")
            # Perform cleanup here
            csv_file.close()
            sys.exit(0)
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            timeout += 1
            print(f'\nTimeout: {timeout}, restarting stream...')
            # Add a delay before retrying
            time.sleep(5)  # adjust this value according to your needs


# ------------------------------------------- RUN ----------------------------------------------------------- #


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sample Twitter Stream, get 1% of current tweets')

    parser.add_argument('--iter_max', type=int, default=1_000_000, help='Maximum number of tweets to get per language')
    parser.add_argument('--languages', type=str, nargs='+', default=['en', 'fr', 'es', 'de', 'it'],
                        help='Languages to get')
    parser.add_argument('--env', type=str, required=True, help='Path to env file, containing bearer token')

    args = parser.parse_args()

    iter_max = args.iter_max
    languages = args.languages
    env = args.env
    bearer_token = get_bearer_token(env)

    iter_ = {}
    for lang in languages:
        iter_[lang] = 0

    date = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = '../../data/sample-stream/' + date + '.csv'

    if not os.path.exists('../../data/sample-stream'):
        os.makedirs('../../data/sample-stream')

    if not os.path.exists(filename):
        csv_file = open(filename, 'w+', encoding='utf-8')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['tweet_id', 'user_id', 'timestamp', 'text', 'lang'])
    else:
        csv_file = open(filename, 'a+', encoding='utf-8')
        csv_writer = csv.writer(csv_file)

    main()

import requests
import os
import json
import csv
from env import get_bearer_token
import datetime
import sys
import traceback
import argparse




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
            csv_writer.writerow([tweet_id, author_id, timestamp, text, lang, class_])
            iter_[lang] += 1
            sys.stdout.write('\r')
            msg = f'{" ".join([f"{l}: {iter_[l]}"  for l in iter_])}'
            sys.stdout.write(msg)



def main():
    url = create_url()
    timeout = 0
    while True:
        connect_to_endpoint(url)
        timeout += 1
        print(f'\nTimeout: {timeout}, restarting stream...')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sample Twitter Stream, get 1% of current tweets')

    parser.add_argument('--iter_max', type=int, default=1_000_000, help='Maximum number of tweets to get per language')
    parser.add_argument('--languages', type=str, nargs='+', default=['en', 'fr', 'es', 'de', 'it'], help='Languages to get')
    parser.add_argument('--env', type=str, required=True, help='Path to env file, containing bearer token')
    parser.add_argument('--class_', type=str, default='3', help='Class of the tweets (Default: 3)')

    args = parser.parse_args()

    iter_max = args.iter_max
    languages = args.languages
    env = args.env
    class_ = args.class_
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
        csv_writer.writerow(['tweet_id', 'user_id', 'timestamp', 'text', 'lang', 'class'])
    else:
        csv_file = open(filename, 'a+', encoding='utf-8')
        csv_writer = csv.writer(csv_file)

    main()

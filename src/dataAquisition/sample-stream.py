import requests
import os
import json
import emoji
import csv
from env import get_bearer_token
import datetime
import sys
import flag
import traceback

bearer_token = get_bearer_token('../botz.env')
print(bearer_token)
iter_max = 1_000_000
languages = ['en', 'fr', 'es', 'de', 'it']
iter_ = {
    'en': 0,
    'fr': 0,
    'es': 0,
    'de': 0,
    'it': 0
}

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
            csv_writer.writerow([tweet_id, author_id, timestamp, text, lang, '3'])
            iter_[lang] += 1
            sys.stdout.write('\r')
            sys.stdout.write(flag.flagize(
                f':US: {iter_["en"]}\t:FR: {iter_["fr"]}\t:ES: {iter_["es"]}\t:DE: {iter_["de"]}\t:IT: {iter_["it"]}\t'))


def main():
    url = create_url()
    timeout = 0
    while True:
        try:
            connect_to_endpoint(url)
        except:
            print(f'\n{traceback.format_exc()}')
            timeout += 1


if __name__ == "__main__":
    main()

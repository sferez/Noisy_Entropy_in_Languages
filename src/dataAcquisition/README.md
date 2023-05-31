# Data Acquisition

Collect data from Twitter using scraping, streaming and Twitter API.

## Scraping

To scrape data from Twitter, run the following file:

```
src/dataAcquisition/run-scraping.py
```

With the following arguments:

```
--from_account: Account to monitor
--env: Environment to use with username, password and email
--start: Start date of the scraping
--end: End date of the scraping
--interval: Interval of the scraping (Default: 1 day)
--headless: Run the scraping in headless mode 
--class_: Flag to indicate if the scraping is for a class (Default: 1)
--only_id: Flag to indicate if only the tweet id should be scraped
```

The data will be saved in the following path:

```
data/<user>/<user>_<start>_<end>.csv
```

The data will be saved in the following format:

```
tweet_id,user_id,timestamp,text,class
```

Command example:

```
python3 src/dataAcquisition/run-scraping.py --from_account elonmusk --env .env --start 2020-01-01 --end 2023-01-01  --headless
```

Note: Languages are not collected by scraping. You can add the language by hydrating the tweets (see below), or by applying a nlp model to the text.

## Streaming

To stream data from Twitter (gather data in real time, 1% of current tweet), run the following file:

```
src/dataAcquisition/sample-stream.py
```

With the following arguments:

```
--env: Environment to use with bearer token
--languages: Languages to stream (Default: en, fr, es, de, it)
--iter_max: Maximum number of iterations for each language (Default: 1_000_000)
--class_: Flag to indicate if the scraping is for a class (Default: 3)
```

The data will be saved in the following path:

```
data/sample_stream/<date>.csv
```

The data will be saved in the following format:

```
tweet_id,user_id,timestamp,text,lang,class
```

Command example:

```
python3 src/dataAcquisition/sample-stream.py --env .env 
```

Note: Class is set to 3 (stream)

## Covid-19

Gather data from the covid-19 github repository and rehydrate the tweets, run the following file:

```
src/dataAcquisition/scrape-covid-github.py
```

With the following arguments:

```
--env: Environment to use with credentials (access_token, access_token_secret, consumer_key, consumer_secret)
--start: Start date of the scraping (Default: 2020-03-22)
--end: End date of the scraping (Default: 2023-04-12)
--class_: Flag to indicate if the scraping is for a class (Default: 4)
```

The data will be saved in the following path:

```
data/covid_github/<date>.csv
```

The data will be saved in the following format:

```
tweet_id,user_id,timestamp,text,lang,class
```

Command example:

```
python3 src/dataAcquisition/scrape-covid-github.py --env .env --start 2020-03-22 --end 2021-01-01
```

Note: Class is set to 4 (covid-19), only LANGUAGES = ['en', 'fr', 'es', 'de', 'it'] are kept. You can change the languages in the code.

## Hydrate Tweets

To hydrate a csv file containing tweet_id, run the following file:

```
src/dataAcquisition/hydrate-tweets.py
```

With the following arguments:

```
--env: Environment to use with credentials (access_token, access_token_secret, consumer_key, consumer_secret)
--file: File to hydrate (CSV with a column named tweet_id)
--class_: Flag to indicate if the scraping is for a class (Default: 1)
```

The data will be saved in the following path:

```
<file>_hydrated.csv
```

The data will be saved in the following format:

```
tweet_id,user_id,timestamp,text,lang,class
```

Command example:

```
python3 src/dataAcquisition/hydrate-tweets.py --env .env --file data/elonmusk/elonmusk_2020-01-01_2023-01-01.csv
```


## Class:

1 - Personalities
2 - News and Media
3 - Stream
4 - Covid-19

## Data Storage

Data is stored in the following structure:

```
├── data
│   ├── <scraping> (Scrape from user, hashtag or keyword)
│   │   ├── <user>
│   │   │   ├── <user>_<start>_<end>.csv
│   │   │   ├── <user>_<start>_<end>.csv
│   │   │   └── ...
│   │   ├── <user>
│   │   │   ├── <user>_<start>_<end>.csv
│   │   │   ├── <user>_<start>_<end>.csv
│   │   │   └── ...
│   │   └── ...
│   ├── <sample-stream> (Stream 1% of tweets)
│   │   ├── <date>.csv
│   │   ├── <date>.csv
│   │   └── ...
│   ├── <covid-github> (Scrape from Github and rehydrate)
│   │   ├── <date>.csv
│   │   ├── <date>.csv
│   │   └── ...
│   └──
└──
```


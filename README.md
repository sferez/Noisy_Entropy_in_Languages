# Noisy_Entropy_Estimation

Project is in development.

## Data Acquisition

### Scraping

To scrape data from Twitter, run the following file:

```
dataAcquisition/run-scraping.py
```

With the following arguments:

```
--from_account: Account to monitor
--env: Environment to use
--start: Start date of the scraping
--end: End date of the scraping
--interval: Interval of the scraping (Default: 1 day)
--headless: Run the scraping in headless mode (Default: False)
--class_: Flag to indicate if the scraping is for a class (Default: 1)
```

The data will be saved in the following path:

```
data/<user>/<user>_<start>_<end>.csv
```

The data will be saved in the following format:

```
tweet_id,user_id,timestamp,text,lang,class
```

Note: From scraping the language can not be determined, so it is set to 'und' (undefined).

### Streaming

To stream data from Twitter (gather data in real time, 1% of current tweet), run the following file:

```
dataAcquisition/sample-stream.py
```

With the following arguments:

```
--env: Environment to use with bearer token
--languages: Languages to stream (Default: en, fr, es, de, it)
--iter_max: Maximum number of iterations for each language (Default: 1_000_000)
```

The data will be saved in the following path:

```
data/sample_stream/<date>.csv
```

The data will be saved in the following format:

```
tweet_id,user_id,timestamp,text,lang,class
```

Note: Class is set to 3 (stream)

### Covid-19

Gather data from the covid-19 github repository and rehydrate the tweets, run the following file:

```
dataAcquisition/scrape-covid-github.py
```

With the following arguments:

```
--env: Environment to use with credentials
--start: Start date of the scraping (Default: 2020-05-20)
--end: End date of the scraping (Default: 2023-04-12)
```

The data will be saved in the following path:

```
data/covid_github/<date>.csv
```

The data will be saved in the following format:

```
tweet_id,user_id,timestamp,text,lang,class
```

Note: Class is set to 4 (covid-19), if the language is accessible from the github repository a filter will be applied to
only keep the tweets in the specified languages (en, fr, es, de, it).

## Class:

### 1 - Personality

### 2 - News and Media

### 3 - Stream

### 4 - Covid-19
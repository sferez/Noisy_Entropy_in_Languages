# Noisy_Entropy_Estimation

Project is in development.

Master's Thesis: Undertook an in-depth study on Noisy Entropy Estimation across multiple languages, utilizing data sourced from Social Media platforms and Computer Language.

## Data

To comply with Twitter's Terms of Service, the data used in this project is only shared dehydrated. Which means that the data is shared in the form of tweet ids, and not the full tweet.

A script to hydrate the data is provided in the [dataAcquisition](https://github.com/sferez/Noisy_Entropy_Estimation/tree/main/src/dataAcquisition) folder, as well as a script to dehydrate the data.

## Data Acquisition

Collect data from Twitter using scraping, streaming and Twitter API.

Learn more about the data collection [here](https://github.com/sferez/Noisy_Entropy_Estimation/tree/main/src/dataAcquisition).

## Preprocessing

In progress...

## NLP

In progress...

## Analysis

In progress...

## Entropy Estimation

In progress...

## Structure

Project is structured as follows:

```
├── data
├── src
│   ├── dataAcquisition
│   ├── preprocessing
│   ├── nlp
│   ├── analysis
│   ├── entropyEstimation
├── docs 
└──
```

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


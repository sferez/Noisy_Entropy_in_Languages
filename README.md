# Noisy_Entropy_Estimation

Project is in development.

Master's Thesis: Undertook an in-depth study on Noisy Entropy Estimation across multiple languages, utilizing data sourced from Social Media platforms and Computer Language.

## Data

The data use for this project is a mix of Social Media data and Computer Language data.

### Social Media Data

For the Social Media data, Twitter was used as the main source. The data was collected using scraping, streaming and Twitter API.

To comply with Twitter's Terms of Service, the data used in this project is only shared dehydrated. Which means that the data is shared in the form of tweet ids, and not the full tweet.

A script to hydrate the data is provided in the [dataAcquisition](https://github.com/sferez/Noisy_Entropy_Estimation/tree/main/src/dataAcquisition) folder, as well as a script to dehydrate the data.

### Computer Language Data

For the Computer Language data, CodeNet was used as the main source. CodeNet is a large-scale, high-quality dataset of programmatic source code. It contains 14M code samples from 55 programming languages, and is available for download [here](https://dax-cdn.cdn.appdomain.cloud/dax-project-codenet/1.0.0/Project_CodeNet.tar.gz).

Due to different License restrictions, the dataset was not created by scratch using GitHub data. Instead, the dataset was downloaded from the official website and used as is.

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


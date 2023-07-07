"""
Run the preliminary analysis on a dataset to explore the data.
"""

# -------------------------------------------------- IMPORTS -------------------------------------------------- #

import os
import re
import string

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from wordcloud import WordCloud
from collections import Counter
from nltk.corpus import stopwords
import nltk
import numpy as np

# -------------------------------------------------- GLOBALS -------------------------------------------------- #

sns.set_theme(style="darkgrid")

sentiment_id = {
    -1: "Negative",
    0: "Neutral",
    1: "Positive",
}

emotion_id = {
    0: 'anger',
    1: 'anticipation',
    2: 'disgust',
    3: 'fear',
    4: 'joy',
    5: 'love',
    6: 'optimism',
    7: 'pessimism',
    8: 'sadness',
    9: 'surprise',
    10: 'trust'
}

offensive_id = {
    0: "Not offensive",
    1: "Offensive"
}

hate_id = {
    0: "Not hate speech",
    1: "Hate speech"
}

irony_id = {
    0: "Not ironic",
    1: "Ironic"
}

topic_id = {
    0: "und",
    1: "arts_&_culture",
    2: "business_&_entrepreneurs",
    3: "celebrity_&_pop_culture",
    4: "diaries_&_daily_life",
    5: "family",
    6: "fashion_&_style",
    7: "film_tv_&_video",
    8: "fitness_&_health",
    9: "food_&_dining",
    10: "gaming",
    11: "learning_&_educational",
    12: "music",
    13: "news_&_social_concern",
    14: "other_hobbies",
    15: "relationships",
    16: "science_&_technology",
    17: "sports",
    18: "travel_&_adventure",
    19: "youth_&_student_life",
}

filename = ""


# -------------------------------------------------- FUNCTIONS -------------------------------------------------- #

def load_data(file):
    global filename
    df = pd.read_csv(file)
    filename = os.path.basename(file)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    for col in ['sentiment', 'emotion', 'offensive', 'hate', 'irony', 'topic']:
        if col in df.columns:
            df[col] = df[col].map(eval(col + '_id'))
    return df


def general_informations(df, save=False):
    print(f'Number of tweets: {len(df)}')
    print('Time range:', df['timestamp'].min().strftime('%Y-%m-%d %H:%M:%S'), 'to',
          df['timestamp'].max().strftime('%Y-%m-%d %H:%M:%S'))

    if save:
        with open(f'../../Final/Analysis/{filename[:-4]}/analysis.txt', 'a+') as f:
            f.write(f'\nGeneral informations\n')
            f.write(f'Number of tweets: {len(df)}\n')
            f.write(
                f'Time range: {df["timestamp"].min().strftime("%Y-%m-%d %H:%M:%S")} to {df["timestamp"].max().strftime("%Y-%m-%d %H:%M:%S")}\n')


def tweets_per_user(df, save=False):
    # Count the number of tweets per user
    user_tweet_counts = df['user_id'].value_counts()

    print(f'Number of users: {len(user_tweet_counts)}')
    print(f'Mean number of tweets per user: {user_tweet_counts.mean()}')
    print(f'Median number of tweets per user: {user_tweet_counts.median()}')
    print(f'Min number of tweets per user: {user_tweet_counts.min()}')
    print(f'Max number of tweets per user: {user_tweet_counts.max()}')
    print(f'Number of users with more than 10 tweets: {len(user_tweet_counts[user_tweet_counts > 10])}')
    print(f'Number of users with more than 100 tweets: {len(user_tweet_counts[user_tweet_counts > 100])}')

    if save:
        with open(f'../../Final/Analysis/{filename[:-4]}/analysis.txt', 'a+') as f:
            f.write(f'\nTweets per user\n')
            f.write(f'Number of users: {len(user_tweet_counts)}\n')
            f.write(f'Mean number of tweets per user: {user_tweet_counts.mean()}\n')
            f.write(f'Median number of tweets per user: {user_tweet_counts.median()}\n')
            f.write(f'Min number of tweets per user: {user_tweet_counts.min()}\n')
            f.write(f'Max number of tweets per user: {user_tweet_counts.max()}\n')
            f.write(f'Number of users with more than 10 tweets: {len(user_tweet_counts[user_tweet_counts > 10])}\n')
            f.write(f'Number of users with more than 100 tweets: {len(user_tweet_counts[user_tweet_counts > 100])}\n')

    # Plot the distribution of the number of tweets per user
    plt.figure(figsize=(15, 6))
    sns.histplot(user_tweet_counts, bins=100)
    plt.title('Distribution of the number of tweets per user')
    plt.xlabel('Number of tweets')
    plt.ylabel('Number of users')
    plt.yscale('log')
    plt.annotate('File: ' + filename,
                 xy=(0, 0), xycoords='axes fraction', fontsize=10, color='grey', alpha=0.8,
                 xytext=(0.02, 0.02), textcoords='axes fraction',
                 horizontalalignment='left', verticalalignment='bottom')
    plt.tight_layout()
    if save:
        plt.savefig(f'../../Final/Analysis/{filename[:-4]}/tweets_per_user_distribution.png')
    plt.show()


def plot_distribution_label(df, save=False):
    for col in ['sentiment', 'emotion', 'offensive', 'hate', 'irony', 'topic', 'lang']:
        if col in df.columns:
            plt.figure(figsize=(10, 6))
            sns.countplot(data=df, x=col)
            plt.title(f'Distribution of {col}')
            plt.annotate('File: ' + filename,
                         xy=(0, 0), xycoords='axes fraction', fontsize=10, color='grey', alpha=0.8,
                         xytext=(0.02, 0.02), textcoords='axes fraction',
                         horizontalalignment='left', verticalalignment='bottom')
            plt.tight_layout()
            if col == 'topic':
                plt.xticks(rotation=90)
            if save:
                plt.savefig(f'../../Final/Analysis/{filename[:-4]}/{col}_distribution.png', bbox_inches='tight')
            plt.show()


def plot_tweets_over_time(df, save=False):
    df['date'] = df['timestamp'].dt.date
    plt.figure(figsize=(15, 6))
    sns.barplot(data=df.groupby('date').count()['tweet_id'].reset_index(), x='date', y='tweet_id', color='gray')
    plt.axhline(df.groupby('date').count()['tweet_id'].mean(), color='red', linestyle='--', label='Mean')
    plt.title('Number of tweets over time')
    plt.xlabel('Date')
    plt.xticks(rotation=45)
    plt.ylabel('Number of tweets')
    plt.annotate('File: ' + filename,
                 xy=(0, 0), xycoords='axes fraction', fontsize=10, color='grey', alpha=0.8,
                 xytext=(0.02, 0.02), textcoords='axes fraction',
                 horizontalalignment='left', verticalalignment='bottom')
    plt.tight_layout()
    df.drop('date', axis=1, inplace=True)
    if save:
        plt.savefig(f'../../Final/Analysis/{filename[:-4]}/tweets_over_time.png')
    plt.show()


def is_punctuation(token):
    return True if token in string.punctuation or token in ("...", '`', "'", "—", '”', '“', "’") else False


def plot_token_frequencies(df, vocab_size, save=False):
    # Calculate the percentage of tokens that fall into each category
    categories = [1, 2, 3, 4, 5, 10, 100]
    percentages = [len(df[df["count"] <= cat]) / vocab_size * 100 for cat in categories]

    # Create a DataFrame for the plot
    plot_df = pd.DataFrame({
        'Category': ['1', '<=2', '<=3', '<=4', '<=5', '<=10', '<=100'],
        'Percentage': percentages
    })

    # Plot
    plt.figure(figsize=(10, 6))
    sns.barplot(data=plot_df, x='Category', y='Percentage', color='gray')
    plt.title('Percentage of Tokens by Frequency Category')
    plt.xlabel('Frequency Category')
    plt.ylabel('Percentage of Tokens (%)')
    if save:
        plt.savefig(f'../../Final/Analysis/{filename[:-4]}/token_appearance.png')
    plt.show()


def analyse_tokens(token_file, save=False):
    nltk.download('stopwords')
    stopwords = nltk.corpus.stopwords.words()

    # Load all the tokens
    with open(token_file, 'r') as f:
        tokens = f.read().splitlines()
    counter = Counter(tokens)

    # Create a DataFrame from the counter
    df = pd.DataFrame.from_dict(counter, orient='index').reset_index()
    df = df.rename(columns={'index': 'token', 0: 'count'})

    vocab = set(tokens)
    print(f'Total number of tokens: {len(tokens)}')
    print(f'Vocabulary size: {len(vocab)}')
    print(f'Number of tokens that only appear:')
    print(f'\t1: {len(df[df["count"] <= 1])}, {len(df[df["count"] <= 1]) / len(vocab) * 100:.2f}%')
    print(f'\t<=2: {len(df[df["count"] <= 2])}, {len(df[df["count"] <= 2]) / len(vocab) * 100:.2f}%')
    print(f'\t<=3: {len(df[df["count"] <= 3])}, {len(df[df["count"] <= 3]) / len(vocab) * 100:.2f}%')
    print(f'\t<=4: {len(df[df["count"] <= 4])}, {len(df[df["count"] <= 4]) / len(vocab) * 100:.2f}%')
    print(f'\t<=5: {len(df[df["count"] <= 5])}, {len(df[df["count"] <= 5]) / len(vocab) * 100:.2f}%')
    print(f'\t<=10: {len(df[df["count"] <= 10])}, {len(df[df["count"] <= 10]) / len(vocab) * 100:.2f}%')
    print(f'\t<=100: {len(df[df["count"] <= 100])}, {len(df[df["count"] <= 100]) / len(vocab) * 100:.2f}%')

    plot_token_frequencies(df, len(vocab), save=save)

    if save:
        with open(f'../../Final/Analysis/{filename[:-4]}/analysis.txt', 'a+') as f:
            f.write(f'\nVocabulary statistics:\n')
            f.write(f'Total number of tokens: {len(tokens)}\n')
            f.write(f'Vocabulary size: {len(vocab)}\n')
            f.write(f'Number of tokens that only appear:\n')
            f.write(f'\t1: {len(df[df["count"] <= 1])}, {len(df[df["count"] <= 1]) / len(vocab) * 100:.2f}%\n')
            f.write(f'\t<=2: {len(df[df["count"] <= 2])}, {len(df[df["count"] <= 2]) / len(vocab) * 100:.2f}%\n')
            f.write(f'\t<=3: {len(df[df["count"] <= 3])}, {len(df[df["count"] <= 3]) / len(vocab) * 100:.2f}%\n')
            f.write(f'\t<=4: {len(df[df["count"] <= 4])}, {len(df[df["count"] <= 4]) / len(vocab) * 100:.2f}%\n')
            f.write(f'\t<=5: {len(df[df["count"] <= 5])}, {len(df[df["count"] <= 5]) / len(vocab) * 100:.2f}%\n')
            f.write(f'\t<=10: {len(df[df["count"] <= 10])}, {len(df[df["count"] <= 10]) / len(vocab) * 100:.2f}%\n')
            f.write(f'\t<=100: {len(df[df["count"] <= 100])}, {len(df[df["count"] <= 100]) / len(vocab) * 100:.2f}%\n')

    # Plot distribution of token frequencies
    plt.figure(figsize=(10, 6))
    sns.histplot(df['count'], bins=100)
    plt.title('Distribution of token frequencies')
    plt.xlabel('Occurrence of token')
    plt.yscale('log')
    plt.annotate('File: ' + filename,
                 xy=(0, 0), xycoords='axes fraction', fontsize=10, color='grey', alpha=0.8,
                 xytext=(0.02, 0.02), textcoords='axes fraction',
                 horizontalalignment='left', verticalalignment='bottom')
    plt.tight_layout()
    if save:
        plt.savefig(f'../../Final/Analysis/{filename[:-4]}/token_frequencies.png')
    plt.show()

    # Plot violin plot
    plt.figure(figsize=(10, 6))
    sns.violinplot(df['count'])
    plt.title('Distribution of token frequencies')
    plt.xlabel('Occurrence of token')
    plt.annotate('File: ' + filename,
                 xy=(0, 0), xycoords='axes fraction', fontsize=10, color='grey', alpha=0.8,
                 xytext=(0.02, 0.02), textcoords='axes fraction',
                 horizontalalignment='left', verticalalignment='bottom')
    plt.tight_layout()
    if save:
        plt.savefig(f'../../Final/Analysis/{filename[:-4]}/token_frequencies_violin.png')
    plt.show()

    print(f'\nMost common tokens:')
    print(df.sort_values('count', ascending=False).head(10))

    if save:
        with open(f'../../Final/Analysis/{filename[:-4]}/analysis.txt', 'a+') as f:
            f.write(f'\nMost common tokens:\n')
            f.write(f'{df.sort_values("count", ascending=False).head(10)}\n')

    # Create a word cloud
    wordcloud = WordCloud(width=800, height=400, max_words=100, background_color='white').generate_from_frequencies(
        counter)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word cloud')
    plt.annotate('File: ' + filename,
                 xy=(0, 0), xycoords='axes fraction', fontsize=10, color='grey', alpha=0.8,
                 xytext=(0.02, 0.02), textcoords='axes fraction',
                 horizontalalignment='left', verticalalignment='bottom')
    plt.tight_layout()
    if save:
        plt.savefig(f'../../Final/Analysis/{filename[:-4]}/wordcloud.png')
    plt.show()

    # Remove punctuation symbols
    df['is_punctuation'] = df['token'].apply(is_punctuation)
    df = df[df['is_punctuation'] == False]
    df.drop('is_punctuation', axis=1, inplace=True)
    counter = {token: freq for token, freq in counter.items() if not is_punctuation(token)}
    print(f'\nMost common tokens without punctuation:')
    print(f"{df.sort_values('count', ascending=False).head(10)}\n")

    if save:
        with open(f'../../Final/Analysis/{filename[:-4]}/analysis.txt', 'a+') as f:
            f.write('\nMost common tokens without punctuation:\n')
            f.write(f"{df.sort_values('count', ascending=False).head(10).to_string()}\n")

    wordcloud = WordCloud(width=800, height=400, max_words=100, background_color='white').generate_from_frequencies(
        counter)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word cloud without punctuation')
    plt.annotate('File: ' + filename,
                 xy=(0, 0), xycoords='axes fraction', fontsize=10, color='grey', alpha=0.8,
                 xytext=(0.02, 0.02), textcoords='axes fraction',
                 horizontalalignment='left', verticalalignment='bottom')
    plt.tight_layout()
    if save:
        plt.savefig(f'../../Final/Analysis/{filename[:-4]}/wordcloud_wo_punctuation.png')
    plt.show()

    # Remove stopwords
    counter = {token: freq for token, freq in counter.items() if token not in stopwords}
    df = df[~df['token'].isin(stopwords)]
    print(f'\nMost common tokens without stopwords:')
    print(df.sort_values('count', ascending=False).head(10))

    if save:
        with open(f'../../Final/Analysis/{filename[:-4]}/analysis.txt', 'a+') as f:
            f.write('\nMost common tokens without stopwords:\n')
            f.write(f"{str(df.sort_values('count', ascending=False).head(10))}\n")

    wordcloud = WordCloud(width=800, height=400, max_words=100, background_color='white').generate_from_frequencies(
        counter)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word cloud without stopwords')
    plt.annotate('File: ' + filename,
                 xy=(0, 0), xycoords='axes fraction', fontsize=10, color='grey', alpha=0.8,
                 xytext=(0.02, 0.02), textcoords='axes fraction',
                 horizontalalignment='left', verticalalignment='bottom')
    plt.tight_layout()
    if save:
        plt.savefig(f'../../Final/Analysis/{filename[:-4]}/wordcloud_wo_stopwords.png')
    plt.show()


def analyse_ppm(ppm_file, save=False):
    with open(ppm_file, 'r') as f:
        line = f.read().splitlines()

    lenghts = []
    for l in line:
        lenghts.append(len(l.split(',')))

    # plot distribution of lenghts
    plt.figure(figsize=(10, 6))
    sns.histplot(lenghts, bins=100)
    plt.title('Distribution of tweet lenghts')
    plt.xlabel('Number of tokens')
    plt.ylabel('Number of tweets')
    plt.annotate('File: ' + filename,
                 xy=(0, 0), xycoords='axes fraction', fontsize=10, color='grey', alpha=0.8,
                 xytext=(0.02, 0.02), textcoords='axes fraction',
                 horizontalalignment='left', verticalalignment='bottom')
    plt.tight_layout()
    if save:
        plt.savefig(f'../../Final/Analysis/{filename[:-4]}/tweet_lenghts.png')
    plt.show()

    # plot violin plot
    plt.figure(figsize=(10, 6))
    sns.violinplot(lenghts)
    plt.title('Distribution of tweet lenghts')
    plt.xlabel('Number of tokens')
    plt.annotate('File: ' + filename,
                 xy=(1, 1), xycoords='axes fraction', fontsize=10, color='grey', alpha=0.8,
                 xytext=(0.02, 0.02), textcoords='axes fraction',
                 horizontalalignment='left', verticalalignment='bottom')
    plt.tight_layout()
    if save:
        plt.savefig(f'../../Final/Analysis/{filename[:-4]}/tweet_lenghts_violin.png')
    plt.show()

    # print statistics
    print(f'Mean number of tokens per tweet: {np.mean(lenghts)}')
    print(f'Median number of tokens per tweet: {np.median(lenghts)}')
    print(f'Std number of tokens per tweet: {np.std(lenghts)}')
    print(f'Q1 number of tokens per tweet: {np.quantile(lenghts, 0.25)}')
    print(f'Q3 number of tokens per tweet: {np.quantile(lenghts, 0.75)}')
    print(f'Min number of tokens per tweet: {np.min(lenghts)}')
    print(f'Max number of tokens per tweet: {np.max(lenghts)}')

    if save:
        with open(f'../../Final/Analysis/{filename[:-4]}/analysis.txt', 'a+') as f:
            f.write(f'\nLenghts statistics:\n')
            f.write(f'\tMean number of tokens per tweet: {np.mean(lenghts)}\n')
            f.write(f'\tMedian number of tokens per tweet: {np.median(lenghts)}\n')
            f.write(f'\tStd number of tokens per tweet: {np.std(lenghts)}\n')
            f.write(f'\tQ1 number of tokens per tweet: {np.quantile(lenghts, 0.25)}\n')
            f.write(f'\tQ3 number of tokens per tweet: {np.quantile(lenghts, 0.75)}\n')
            f.write(f'\tMin number of tokens per tweet: {np.min(lenghts)}\n')
            f.write(f'\tMax number of tokens per tweet: {np.max(lenghts)}\n')


def map_sentiment(sentiment):
    if sentiment == 'Neutral':
        return 0
    elif sentiment == 'Positive':
        return 1
    elif sentiment == 'Negative':
        return -1


def plot_sentiment_over_time(df, save=False):
    if 'sentiment' not in df.columns:
        return
    df['date'] = df['timestamp'].dt.date
    df['sentiment_id'] = df['sentiment'].apply(map_sentiment)
    df_grouped = df.groupby('date')['sentiment_id'].mean().reset_index()

    # Plot
    plt.figure(figsize=(15, 6))
    sns.lineplot(data=df_grouped, x='date', y='sentiment_id')
    plt.axhline(y=df_grouped['sentiment_id'].mean(), color='r', linestyle='--', label='Mean sentiment')
    plt.title('Average Sentiment Over Time')
    plt.xlabel('Date')
    plt.ylabel('Average Sentiment')
    plt.annotate('File: ' + filename,
                 xy=(0, 0), xycoords='axes fraction', fontsize=10, color='grey', alpha=0.8,
                 xytext=(0.02, 0.02), textcoords='axes fraction',
                 horizontalalignment='left', verticalalignment='bottom')
    plt.tight_layout()
    if save:
        plt.savefig(f'../../Final/Analysis/{filename[:-4]}/sentiment_over_time.png')
    plt.show()

    df.drop('date', axis=1, inplace=True)
    df.drop('sentiment_id', axis=1, inplace=True)


def plot_by_day(df, save=False):
    # Create a new column for hour of the day
    df['hour'] = df['timestamp'].dt.hour

    # Plot number of tweets by hour of the day
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='hour', color='gray')
    plt.axhline(y=np.mean(df['hour'].value_counts()), color='red', linestyle='--', label='Mean')
    plt.title('Number of Tweets by Hour of the Day')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Number of Tweets')
    plt.annotate('File: ' + filename,
                 xy=(0, 0), xycoords='axes fraction', fontsize=10, color='grey', alpha=0.8,
                 xytext=(0.02, 0.02), textcoords='axes fraction',
                 horizontalalignment='left', verticalalignment='bottom')
    plt.tight_layout()
    if save:
        plt.savefig(f'../../Final/Analysis/{filename[:-4]}/tweets_by_hour.png')
    plt.show()


# -------------------------------------------------- MAIN -------------------------------------------------- #


def run_tweet_analysis(file, save=False):
    if save:
        os.makedirs(f'../../Final/Analysis/{os.path.basename(file).split(".")[0]}', exist_ok=True)
        open(f'../../Final/Analysis/{os.path.basename(file).split(".")[0]}/analysis.txt', 'w').close()
    df = load_data(file)
    general_informations(df, save)
    tweets_per_user(df, save)
    plot_distribution_label(df, save)
    plot_tweets_over_time(df, save)
    plot_by_day(df, save)
    plot_sentiment_over_time(df, save)

    # get directory name
    dirname = os.path.dirname(file)

    for f in os.listdir(dirname):
        if f.endswith(".txt") and os.path.basename(file).split('.')[0] in f:
            if 'ppm' in f:
                analyse_ppm(os.path.join(dirname, f), save)
            elif 'token' in f:
                analyse_tokens(os.path.join(dirname, f), save)

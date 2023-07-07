"""
Run the preliminary analysis on a dataset to explore the data.
"""

# -------------------------------------------------- IMPORTS -------------------------------------------------- #

import os
import string
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import nltk

# -------------------------------------------------- GLOBALS -------------------------------------------------- #

sns.set_theme(style="darkgrid")

filename = ""


# -------------------------------------------------- FUNCTIONS -------------------------------------------------- #


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


# -------------------------------------------------- MAIN -------------------------------------------------- #


def run_text_analysis(file, save=False):
    global filename
    if save:
        os.makedirs(f'../../Final/Analysis/{os.path.basename(file).split(".")[0]}', exist_ok=True)
        open(f'../../Final/Analysis/{os.path.basename(file).split(".")[0]}/analysis.txt', 'w').close()

    # get directory name
    dirname = os.path.dirname(file)
    filename = os.path.basename(file)

    for f in os.listdir(dirname):
        if f.endswith(".txt") and os.path.basename(file).split('.')[0] in f:
            if 'token' in f and 'ppm' not in f:
                analyse_tokens(os.path.join(dirname, f), save)

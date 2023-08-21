"""
:author: Siméon FEREZ
:version: 1.0.0
:copyright: Copyright © 2023 by Siméon FEREZ. All rights reserved. This work may not be reproduced, in whole or in part, without the written permission of the author.
:description: Performs a preliminary analysis of the code files.
"""

# -------------------------------------------------- IMPORTS -------------------------------------------------- #

# External
import gc
import os
import string
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter

# -------------------------------------------------- GLOBALS -------------------------------------------------- #

sns.set_theme(style="darkgrid")
filename = ""


# -------------------------------------------------- FUNCTIONS -------------------------------------------------- #


def is_punctuation(token):
    """
    Check if a token is a punctuation symbol.

    :param token: The token to check.
    :type token: str
    :return: True if the token is a punctuation symbol, False otherwise.
    :rtype: bool

    >>> is_punctuation("!")
    >>> True
    """
    return True if token in string.punctuation or token in ("...", '`', "'", "—", '”', '“', "’") else False


def is_special_token(token):
    """
    Check if a token is a special token.

    :param token: The token to check.
    :type token: str
    :return: True if the token is a special token, False otherwise.
    :rtype: bool

    >>> is_special_token("#VAR#")
    >>> True
    """
    return True if token in (
        "#VAR#", "#STR#", "#FUNC#", "#COMMENT#", "#NUM#", "#NEWLINE#", "#INDENT#", "#DEDENT#") else False


def plot_token_frequencies(df, vocab_size, save=False):
    """
    Plot the percentage of tokens that fall into each category.

    :param df: The DataFrame containing the tokens and their frequencies.
    :type df: pd.DataFrame
    :param vocab_size: The size of the vocabulary.
    :type vocab_size: int
    :param save: Whether to save the plot or not.
    :type save: bool
    :return: None
    :rtype: None

    >>> plot_token_frequencies(pd.DataFrame({'token': ['a', 'b', 'c'], 'count': [1, 2, 3]}), 3)
    """
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
    """
    Perform a preliminary analysis of the tokens.

    :param token_file: The path to the file containing the tokens.
    :type token_file: str
    :param save: Whether to save the plots or not.
    :type save: bool
    :return: None
    :rtype: None

    >>> analyse_tokens('token.txt')
    """
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

    # Remove special token
    df['is_special'] = df['token'].apply(is_special_token)
    df = df[df['is_special'] == False]
    df.drop('is_special', axis=1, inplace=True)
    counter = {token: freq for token, freq in counter.items() if not is_special_token(token)}
    print(f'\nMost common tokens without special tokens:')
    print(df.sort_values('count', ascending=False).head(10))

    if save:
        with open(f'../../Final/Analysis/{filename[:-4]}/analysis.txt', 'a+') as f:
            f.write('\nMost common tokens without special tokens:\n')
            f.write(f"{str(df.sort_values('count', ascending=False).head(10))}\n")

    wordcloud = WordCloud(width=800, height=400, max_words=100, background_color='white').generate_from_frequencies(
        counter)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word cloud without special tokens')
    plt.annotate('File: ' + filename,
                 xy=(0, 0), xycoords='axes fraction', fontsize=10, color='grey', alpha=0.8,
                 xytext=(0.02, 0.02), textcoords='axes fraction',
                 horizontalalignment='left', verticalalignment='bottom')
    plt.tight_layout()
    if save:
        plt.savefig(f'../../Final/Analysis/{filename[:-4]}/wordcloud_wo_specialtokens.png')
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


def analyse_ppm(ppm_file, save=False):
    """
    Perform a preliminary analysis of the ppm file.

    :param ppm_file: The path to the file containing the ppm.
    :type ppm_file: str
    :param save: Whether to save the plots or not.
    :type save: bool
    :return: None
    :rtype: None

    >>> analyse_ppm('ppm.txt')
    """
    with open(ppm_file, 'r') as f:
        line = f.read().splitlines()

    lenghts = []
    for l in line:
        lenghts.append(len(l.split(',')))

    # plot distribution of lenghts
    plt.figure(figsize=(10, 6))
    sns.histplot(lenghts, bins=100)
    plt.title('Distribution of code lenghts')
    plt.xlabel('Number of tokens')
    plt.ylabel('Number of codes')
    plt.annotate('File: ' + filename,
                 xy=(0, 0), xycoords='axes fraction', fontsize=10, color='grey', alpha=0.8,
                 xytext=(0.02, 0.02), textcoords='axes fraction',
                 horizontalalignment='left', verticalalignment='bottom')
    plt.tight_layout()
    if save:
        plt.savefig(f'../../Final/Analysis/{filename[:-4]}/code_lenghts.png')
    plt.show()

    # plot violin plot
    plt.figure(figsize=(10, 6))
    sns.violinplot(lenghts)
    plt.title('Distribution of code lenghts')
    plt.xlabel('Number of tokens')
    plt.annotate('File: ' + filename,
                 xy=(1, 1), xycoords='axes fraction', fontsize=10, color='grey', alpha=0.8,
                 xytext=(0.02, 0.02), textcoords='axes fraction',
                 horizontalalignment='left', verticalalignment='bottom')
    plt.tight_layout()
    if save:
        plt.savefig(f'../../Final/Analysis/{filename[:-4]}/code_lenghts_violin.png')
    plt.show()

    # print statistics
    print(f'Mean number of tokens per code: {np.mean(lenghts)}')
    print(f'Median number of tokens per code: {np.median(lenghts)}')
    print(f'Std number of tokens per code: {np.std(lenghts)}')
    print(f'Q1 number of tokens per code: {np.quantile(lenghts, 0.25)}')
    print(f'Q3 number of tokens per code: {np.quantile(lenghts, 0.75)}')
    print(f'Min number of tokens per code: {np.min(lenghts)}')
    print(f'Max number of tokens per code: {np.max(lenghts)}')

    if save:
        with open(f'../../Final/Analysis/{filename[:-4]}/analysis.txt', 'a+') as f:
            f.write(f'\nLenghts statistics:\n')
            f.write(f'\tMean number of tokens per code: {np.mean(lenghts)}\n')
            f.write(f'\tMedian number of tokens per code: {np.median(lenghts)}\n')
            f.write(f'\tStd number of tokens per code: {np.std(lenghts)}\n')
            f.write(f'\tQ1 number of tokens per code: {np.quantile(lenghts, 0.25)}\n')
            f.write(f'\tQ3 number of tokens per code: {np.quantile(lenghts, 0.75)}\n')
            f.write(f'\tMin number of tokens per code: {np.min(lenghts)}\n')
            f.write(f'\tMax number of tokens per code: {np.max(lenghts)}\n')

    del lenghts, line
    gc.collect()


# -------------------------------------------------- MAIN -------------------------------------------------- #


def run_code_analysis(file, save=False):
    """
    Run the analysis of the code files.

    :param file: The path to the file containing the code.
    :type file: str
    :param save: Whether to save the plots or not.
    :type save: bool
    :return: None
    :rtype: None

    >>> run_code_analysis('code.csv')
    """
    global filename
    if save:
        os.makedirs(f'../../Final/Analysis/{os.path.basename(file).split(".")[0]}', exist_ok=True)
        open(f'../../Final/Analysis/{os.path.basename(file).split(".")[0]}/analysis.txt', 'w').close()

    # get directory name
    dirname = os.path.dirname(file)
    filename = os.path.basename(file)

    for f in os.listdir(dirname):
        if f.endswith(".txt") and os.path.basename(file).split('.')[0] in f:
            if "ppm" in f:
                analyse_ppm(os.path.join(dirname, f), save)
            elif 'token' in f and 'vocab' not in f:
                analyse_tokens(os.path.join(dirname, f), save)

"""
:author: Siméon FEREZ
:version: 1.0.0
:copyright: Copyright © 2023 by Siméon FEREZ. All rights reserved. This work may not be reproduced, in whole or in part, without the written permission of the author.
:description: Clean Twitter CSV files.

CLI Arguments:
    - --input, --i: Directory containing the raw data, or CSV File
    - --output, --o: Directory to save the scraping-cleaned data.
    - --punctuation, --p: Keep punctuation (default: False)
    - --accents, --a: Keep accents (default: False)
    - --emojis, --e: Keep emojis (default: False)
    - --mentions, --m: Keep mentions (default: False)
    - --urls, --u: Keep urls (default: False)
    - --spaces, --s: Keep extra spaces (default: False)
    - --rt, --r: Keep RT Tags (default: False)
    -- -lowercase, --l: Keep all cases (default: False)

Examples:
    >>> python clean_tweets.py --input data.csv --output data-cleaned
    >>> python clean_tweets.py --input data.csv --output data-cleaned --punctuation
    >>> python clean_tweets.py --input data.csv --output data-cleaned --punctuation --accents --emojis
"""

# -------------------------------------------------- IMPORTS -------------------------------------------------- #

# External
import pandas as pd
import os
import re
import emoji
from emot.emo_unicode import EMOTICONS_EMO
import argparse
import string
from unidecode import unidecode
from tqdm import tqdm
from pandas.errors import ParserError


# ------------------------------------------------- FUNCTIONS ------------------------------------------------- #

def remove_emoticons(text):
    """
    Remove emoticons from a text using a regex.

    :param text: text to clean
    :type text: str
    :return: cleaned text
    :rtype: str

    >>> remove_emoticons('I am so happy :)')
    >>> 'I am so happy '
    """
    emoticon_pattern = re.compile(u'(' + u'|'.join(k for k in EMOTICONS_EMO) + u')')
    return emoticon_pattern.sub(r'', text)


def remove_emoji(text):
    """
    Remove emojis from a text using a regex.

    :param text: text to clean
    :type text: str
    :return: cleaned text
    :rtype: str

    >>> remove_emoji('I am so happy 😊')
    >>> 'I am so happy '
    """
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


def remove_urls(text):
    """
    Remove urls from a text using a regex.

    :param text: text to clean
    :type text: str
    :return: cleaned text
    :rtype: str

    >>> remove_urls('I am so happy https://www.google.com')
    >>> 'I am so happy '
    """
    result = re.sub(r"http\S+", "", text)
    # result = re.sub(r'(https?://\S+|www\.\S+)', '', text)
    return result


def remove_twitter_urls(text):
    """
    Remove twitter urls from a text using a regex.

    :param text: text to clean
    :type text: str
    :return: cleaned text
    :rtype: str

    >>> remove_urls('I am so happy pic.twitter.com/123')
    >>> 'I am so happy '
    """
    clean = re.sub(r"pic.twitter\S+", "", text)
    return clean


def give_emoji_free_text(text):
    """
    Remove emojis from a text using the emoji library.

    :param text: text to clean
    :type text: str
    :return: cleaned text
    :rtype: str

    >>> give_emoji_free_text('I am so happy 😊')
    >>> 'I am so happy '
    """
    return emoji.replace_emoji(text, replace="")


def remove_mentions(text):
    """
    Remove mentions from a text using a regex.

    :param text: text to clean
    :type text: str
    :return: cleaned text
    :rtype: str

    >>> remove_mentions('I am so happy @user')
    >>> 'I am so happy '
    """
    return re.sub(r'@\w+', '', text)


def to_lowercase(text):
    """
    Convert a text to lowercase.

    :param text: text to convert
    :type text: str
    :return: converted text
    :rtype: str

    >>> to_lowercase('I am so happy')
    >>> 'i am so happy'
    """
    return text.lower()


def remove_punctuation(text):
    """
    Remove punctuation from a text.

    :param text: text to clean
    :type text: str
    :return: cleaned text
    :rtype: str

    >>> remove_punctuation('I am so happy!')
    >>> 'I am so happy'
    """
    special_chars = "«».`—'“’"
    return text.translate(str.maketrans('', '', string.punctuation + special_chars))


def remove_extra_spaces(text):
    """
    Remove extra spaces from a text.

    :param text: text to clean
    :type text: str
    :return: cleaned text
    :rtype: str

    >>> remove_extra_spaces('I am so    happy')
    >>> 'I am so happy'
    """
    text = text.replace('  ', ' ')  # 2 spaces
    text = text.replace('   ', ' ')  # 3 spaces
    text = text.replace('    ', ' ')  # 4 spaces
    text = text.replace('     ', ' ')  # 5 spaces
    text = text.replace('      ', ' ')  # 6 spaces
    return text


def remove_accents(text):
    """
    Remove accents from a text using the unidecode library.

    :param text: text to clean
    :type text: str
    :return: cleaned text
    :rtype: str

    >>> remove_accents('Ceci est un résumé')
    >>> 'Ceci est un resume'
    """
    return unidecode(text)


def remove_rt(text):
    """
    Remove RT from a text.

    :param text: text to clean
    :type text: str
    :return: cleaned text
    :rtype: str

    >>> remove_rt('RT : I am so happy')
    >>> 'I am so happy'
    """
    if text.startswith('RT : ') and mentions:
        return text[5:]
    elif text.startswith('RT ') and not mentions:
        return text[3:]
    return text


def process_file(fp):
    """
    Process a CSV file and save the cleaned version.

    :param fp: file path
    :type fp: str
    :return: None
    :rtype: None

    >>> process_file('data.csv')
    """
    try:
        df = pd.read_csv(fp, encoding='utf-8')
    except ParserError:
        print(f'ParserError: {fp}')
        df = pd.read_csv(fp, lineterminator='\n', encoding='utf-8')

    df.dropna(subset=['text', 'tweet_id'], inplace=True)
    df.drop_duplicates(subset=['tweet_id'], inplace=True)

    df['tweet_id'] = df['tweet_id'].astype(int)
    df['user_id'].replace('error-co', 0, inplace=True)  # Error in the data (user_id = 'error-co')
    df['user_id'].fillna(0, inplace=True)
    df['user_id'] = df['user_id'].astype(int)

    df['text'] = df['text'].str.replace('\n', '')
    df['text'] = df['text'].str.replace('\r', '')

    if urls:
        df['text'] = df['text'].apply(lambda x: remove_urls(x))
        df['text'] = df['text'].apply(lambda x: remove_twitter_urls(x))
    if emojis:
        df['text'] = df['text'].apply(lambda x: remove_emoji(x))
        df['text'] = df['text'].apply(lambda x: give_emoji_free_text(x))
    if mentions:
        df['text'] = df['text'].apply(lambda x: remove_mentions(x))
    if rt:
        df['text'] = df['text'].apply(lambda x: remove_rt(x))
    if punctuation:
        df['text'] = df['text'].apply(lambda x: remove_punctuation(x))
    if accents:
        df['text'] = df['text'].apply(lambda x: remove_accents(x))
    if spaces:
        df['text'] = df['text'].apply(lambda x: remove_extra_spaces(x))
    if lowercase:
        df['text'] = df['text'].apply(lambda x: to_lowercase(x))

    df.drop(df[df['text'] == ''].index, inplace=True)
    df.to_csv(os.path.join(output_, os.path.basename(fp)), index=False)

    print(f'Cleaned {os.path.basename(fp)}')


# -------------------------------------------------- MAIN -------------------------------------------------- #


def main():
    """
    Main function of the data cleaning script.

    :return: None
    :rtype: None

    >>> main()
    """
    print('Cleaning data...')
    if not os.path.exists(output_):
        os.makedirs(output_)

    if os.path.isfile(input_):
        process_file(input_)
    else:

        for root, dirs, files in os.walk(input_):
            for file in tqdm(files):
                if file.endswith(".csv"):
                    fp = os.path.join(root, file)
                    process_file(fp)


# -------------------------------------------------- CLI -------------------------------------------------- #

if __name__ == '__main__':
    """
    Command Line Interface of the Twitter data cleaning script.
    
    Args:
        --input, --i: Directory containing the raw data, or CSV File
        --output, --o: Directory to save the scraping-cleaned data.
        --punctuation, --p: Keep punctuation (default: False)
        --accents, --a: Keep accents (default: False)
        --emojis, --e: Keep emojis (default: False)
        --mentions, --m: Keep mentions (default: False)
        --urls, --u: Keep urls (default: False)
        --spaces, --s: Keep extra spaces (default: False)
        --rt, --r: Keep RT Tags (default: False)
        --lowercase, --l: Keep all cases (default: False)
        
    Examples:
        >>> python clean_tweets.py --input data.csv --output data-cleaned
        >>> python clean_tweets.py --input data.csv --output data-cleaned --punctuation
        >>> python clean_tweets.py --input data.csv --output data-cleaned --punctuation --accents --emojis
    """
    parser = argparse.ArgumentParser(description='Perform data cleaning on the raw linguistic data.')
    parser.add_argument('--input', '--i', type=str, help='Directory containing the raw data, or CSV File',
                        required=True)
    parser.add_argument('--output', '--o', type=str, help='Directory to save the scraping-cleaned data.', required=True)

    parser.add_argument('--punctuation', '--p', action=argparse.BooleanOptionalAction, help='Keep punctuation',
                        default=False)
    parser.add_argument('--accents', '--a', action=argparse.BooleanOptionalAction, help='Keep accents', default=False)
    parser.add_argument('--emojis', '--e', action=argparse.BooleanOptionalAction, help='Keep emojis', default=False)
    parser.add_argument('--mentions', '--m', action=argparse.BooleanOptionalAction, help='Keep mentions', default=False)
    parser.add_argument('--urls', '--u', action=argparse.BooleanOptionalAction, help='Keep urls', default=False)
    parser.add_argument('--spaces', '--s', action=argparse.BooleanOptionalAction, help='Keep extra spaces',
                        default=False)
    parser.add_argument('--rt', '--r', action=argparse.BooleanOptionalAction, help='Keep RT Tags', default=False)
    parser.add_argument('--lowercase', '--l', action=argparse.BooleanOptionalAction, help='Keep all cases',
                        default=False)

    args = parser.parse_args()

    input_ = args.input
    output_ = args.output
    punctuation = not args.punctuation
    accents = not args.accents
    emojis = not args.emojis
    mentions = not args.mentions
    urls = not args.urls
    spaces = not args.spaces
    rt = not args.rt
    lowercase = not args.lowercase

    main()

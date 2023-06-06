"""
Perform data cleaning on the raw linguistic data (tweets).
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


# ------------------------------------------------- FUNCTIONS ------------------------------------------------- #

def remove_emoticons(text):
    emoticon_pattern = re.compile(u'(' + u'|'.join(k for k in EMOTICONS_EMO) + u')')
    return emoticon_pattern.sub(r'', text)


def remove_emoji(text):
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
    result = re.sub(r"http\S+", "", text)
    return (result)


def remove_twitter_urls(text):
    clean = re.sub(r"pic.twitter\S+", "", text)
    return (clean)


def give_emoji_free_text(text):
    return emoji.replace_emoji(text, replace="")


def remove_mentions(text):
    return re.sub(r'@\w+', '', text)


def to_lowercase(text):
    return text.lower()


def remove_punctuation(text):
    special_chars = "«»"
    return text.translate(str.maketrans('', '', string.punctuation + special_chars))


def remove_extra_spaces(text):
    text = text.replace('  ', ' ')  # 2 spaces
    text = text.replace('   ', ' ')  # 3 spaces
    text = text.replace('    ', ' ')  # 4 spaces
    text = text.replace('     ', ' ')  # 5 spaces
    text = text.replace('      ', ' ')  # 6 spaces
    return text

def remove_accents(text):
    return unidecode(text)


# -------------------------------------------------- MAIN -------------------------------------------------- #


def main():
    full_paths = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".csv"):
                full_paths.append(os.path.join(root, file))

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print('Cleaning data...')
    for fp in full_paths:
        df = pd.read_csv(fp)
        df.dropna()
        df = df.dropna(subset=['text'])
        df['tweet_id'] = df['tweet_id'].astype('int64')
        df['user_id'] = df['user_id'].astype('int64')
        df.drop_duplicates(subset=['tweet_id'], inplace=True)
        df['text'] = df['text'].str.replace('\n', '')
        df['text'] = df['text'].str.replace('\r', '')
        df['text'] = df['text'].apply(lambda x: remove_urls(x))
        df['text'] = df['text'].apply(lambda x: remove_twitter_urls(x))
        df['text'] = df['text'].apply(lambda x: remove_mentions(x))
        df['text'] = df['text'].apply(lambda x: remove_emoji(x))
        df['text'] = df['text'].apply(lambda x: remove_accents(x))
        # df['text'] = df['text'].apply(lambda x: remove_emoticons(x))
        df['text'] = df['text'].apply(lambda x: give_emoji_free_text(x))
        df['text'] = df['text'].apply(lambda x: remove_punctuation(x))
        df['text'] = df['text'].apply(lambda x: remove_extra_spaces(x))
        df['text'] = df['text'].apply(lambda x: to_lowercase(x))

        df.to_csv(os.path.join(output_dir, os.path.basename(fp)), index=False)

        print(f'Cleaned {os.path.basename(fp)}')


# -------------------------------------------------- CLI -------------------------------------------------- #

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Perform data cleaning on the raw linguistic data.')
    parser.add_argument('--input_dir', '--i', type=str, help='Directory containing the raw data.', required=True)
    parser.add_argument('--output_dir', '--o', type=str, help='Directory to save the cleaned data.', required=True)

    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir

    main()

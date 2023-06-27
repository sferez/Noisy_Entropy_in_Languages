"""
Tokenize the raw linguistic data.
"""

# -------------------------------------------------- IMPORTS -------------------------------------------------- #

# External
import argparse
import os
from nltk.tokenize import TweetTokenizer
import pandas as pd
from tqdm import tqdm
from itertools import chain
from nltk.util import ngrams


# ------------------------------------------------- FUNCTIONS ------------------------------------------------- #


def generate_ngrams(tokens, n):
    n_grams = ngrams(tokens, n)
    return [" ".join(gram) for gram in n_grams]


def process_file(fp):
    print(f'Tokenizing {fp}...')
    df = pd.read_csv(fp)
    df = df.dropna(subset=['text'])
    df['text'] = df['text'].astype(str)
    tqdm.pandas()
    if not chars:
        df['tokens'] = df['text'].progress_apply(lambda x: tweet_tokenizer.tokenize(x))
    else:
        df['tokens'] = df['text'].progress_apply(lambda x: list(x))
    if ngrams_ > 1:
        df['tokens'] = df['tokens'].apply(lambda x: generate_ngrams(x, ngrams_))
    all_tokens = list(chain.from_iterable(df['tokens']))
    with open(fp.replace('.csv', f'_vocab_{ngrams_}-gram{"_char" if chars else ""}.txt'), 'w') as f:
        for token in set(all_tokens):
            f.write(f'{token}\n')
        f.close()
    with open(fp.replace('.csv', f'_tokens_{ngrams_}-gram{"_char" if chars else ""}.txt'), 'w') as f:
        for tokens in all_tokens:
            f.write(f'{tokens}\n')
    print(f'Tokenized {fp}.'
          f'\n\tVocab: {fp.replace(".csv", f"_vocab_{ngrams_}-gram.txt")}'
          f'\n\tTokens: {fp.replace(".csv", f"_tokens_{ngrams_}-gram.txt")}')


# ------------------------------------------------- MAIN ------------------------------------------------- #

def main():
    print(f'Tokenizing data with {ngrams_}-grams tokens...')

    if os.path.isfile(input_):
        process_file(input_)
    else:

        for root, dirs, files in os.walk(input_):
            for file in files:
                if file.endswith(".csv"):
                    fp = os.path.join(root, file)
                    process_file(fp)


# -------------------------------------------------- CLI -------------------------------------------------- #

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Perform tokenization on the raw linguistic data.')
    parser.add_argument('--input', '--i', type=str, help='Directory or CSV file', required=True)
    parser.add_argument('--ngrams', '--n', type=int, help='Generate n-grams', default=1)
    parser.add_argument('--chars', '--c', action=argparse.BooleanOptionalAction, help='Use characters instead of words', default=False)

    args = parser.parse_args()

    input_ = args.input
    ngrams_ = args.ngrams
    chars = args.chars

    tweet_tokenizer = TweetTokenizer()

    main()

'''
Tokenize computer language data.
'''

# -------------------------------------------------- IMPORTS -------------------------------------------------- #

# External
from ast import literal_eval
from itertools import chain
import pandas as pd
from tqdm import tqdm
import argparse
import os
import subprocess
from nltk.util import ngrams
import csv

# -------------------------------------------------- GLOBALS -------------------------------------------------- #

CHUNKSIZE = 100000
vocab = set()


# ------------------------------------------------- FUNCTIONS ------------------------------------------------- #


def update_vocab(tokens):
    if not char:
        for token in tokens:
            if token not in vocab:
                vocab.add(token)
    else:
        for c in ''.join(tokens):
            if c not in vocab:
                vocab.add(c)


def generate_ngrams(tokens, n):
    n_grams = ngrams(tokens, n)
    return [" ".join(gram) for gram in n_grams]


def process_file(fp):
    print('Processing...')
    df = pd.read_csv(fp)
    df['tokens'] = df['tokens'].apply(lambda x: literal_eval(x))
    if ngrams_ > 1:
        df['tokens'] = df['tokens'].apply(lambda x: generate_ngrams(x, ngrams_))
    tokens = list(chain.from_iterable(df['tokens']))

    if ppm:
        csv_writer = csv.writer(
            open(fp.replace('.csv', f'_tokens_{ngrams_}-gram{"_char" if char else ""}_ppm.txt'), 'w'))
        for tokens in df["tokens"]:
            csv_writer.writerow(tokens)
    else:
        with open(fp.replace('.csv', f'_tokens_{ngrams_}-gram{"_char" if char else ""}.txt'), 'w') as f:
            if not char:
                for token in tokens:
                    f.write(f'{token}\n')
            else:
                for c in ''.join(tokens):
                    f.write(f'{c}\n')
    with open(fp.replace('.csv', f'_vocab_{ngrams_}-gram{"_char" if char else ""}.txt'), 'w') as f:
        if not char:
            for token in set(tokens):
                f.write(f'{token}\n')
        else:
            for c in set(''.join(tokens)):
                f.write(f'{c}\n')


def process_file_chunk(fp, num_lines):
    print('Processing in chunks...')
    for i, df in tqdm(enumerate(pd.read_csv(fp, chunksize=CHUNKSIZE)),
                      total=num_lines // CHUNKSIZE + 1):
        df['tokens'] = df['tokens'].apply(lambda x: literal_eval(x))
        if ngrams_ > 1:
            df['tokens'] = df['tokens'].apply(lambda x: generate_ngrams(x, ngrams_))
        tokens = list(chain.from_iterable(df['tokens']))

        mode = 'a' if i != 0 else 'w'

        if ppm:
            df["tokens"].to_csv(fp.replace('.csv', f'_tokens_{ngrams_}-gram{"_char" if char else ""}_ppm.txt'),
                                mode=mode, index=False)
        else:
            with open(fp.replace('.csv', f'_tokens_{ngrams_}-gram{"_char" if char else ""}.txt'), mode) as f:
                if not char:
                    for token in tokens:
                        f.write(f'{token}\n')
                else:
                    for c in ''.join(tokens):
                        f.write(f'{c}\n')

        update_vocab(tokens)

    with open(fp.replace('.csv', f'_vocab_{ngrams_}-gram{"_char" if char else ""}.txt'), 'w') as f:
        for token in vocab:
            f.write(f'{token}\n')


# -------------------------------------------------- MAIN -------------------------------------------------- #


def main():
    if os.path.isfile(input_):  # Single file
        num_lines = int(subprocess.check_output(f"wc -l {input_}", shell=True).split()[0]) - 1
        if num_lines > CHUNKSIZE:
            process_file_chunk(input_, num_lines)
        else:
            process_file(input_)
    else:
        for root, dirs, files in os.walk(input_):
            for file in files:
                if file.endswith(".csv"):
                    print(file)
                    num_lines = int(subprocess.check_output(f"wc -l {input_}", shell=True).split()[0]) - 1
                    if num_lines > CHUNKSIZE:
                        process_file_chunk(input_, num_lines)
                    else:
                        process_file(input_)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '--i', type=str, help='Directory or CSV File', required=True)
    parser.add_argument('--char', '--c', action=argparse.BooleanOptionalAction, help='Character-level tokenization',
                        default=False)
    parser.add_argument('--ngrams', '--n', type=int, help='Generate n-grams', default=1)
    parser.add_argument('--ppm', action=argparse.BooleanOptionalAction, help='Write tokens for ppm analysis',
                        default=False)

    args = parser.parse_args()
    input_ = args.input
    char = args.char
    ngrams_ = args.ngrams
    ppm = args.ppm

    main()

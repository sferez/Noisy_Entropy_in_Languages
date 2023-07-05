"""
Tokenize the raw linguistic data from a txt file.
"""

# -------------------------------------------------- IMPORTS -------------------------------------------------- #

# External
import argparse
import os
from nltk.tokenize import TweetTokenizer
from nltk.util import ngrams
import csv


# ------------------------------------------------- FUNCTIONS ------------------------------------------------- #


def generate_ngrams(tokens, n):
    n_grams = ngrams(tokens, n)
    return [" ".join(gram) for gram in n_grams]


def process_file(fp):
    print(f'Tokenizing {fp}...')
    all_tokens = []
    csv_writer = csv.writer(
        open(fp.replace('.txt', f'_tokens_{ngrams_}-gram{"_char" if chars else ""}_ppm.txt'), 'w'))
    with open(fp, 'r') as file:
        for line in file:
            line = line.strip().lower().replace('*', '').replace('','')
            if not chars:
                tokens = tweet_tokenizer.tokenize(line)
            else:
                tokens = list(line)
            if ngrams_ > 1:
                tokens = generate_ngrams(tokens, ngrams_)
            all_tokens.extend(tokens)

            # if not blank line
            if tokens:
                csv_writer.writerow(tokens)

    with open(fp.replace('.txt', f'_tokens_{ngrams_}-gram{"_char" if chars else ""}.txt'), 'w') as f:
        for token in all_tokens:
            f.write(f'{token}\n')

    with open(fp.replace('.txt', f'_vocab_{ngrams_}-gram{"_char" if chars else ""}.txt'), 'w') as f:
        for token in set(all_tokens):
            f.write(f'{token}\n')

    print(f'Tokenized {fp}.')


# ------------------------------------------------- MAIN ------------------------------------------------- #

def main():
    print(f'Tokenizing data with {ngrams_}-grams tokens...')

    if os.path.isfile(input_):
        process_file(input_)
    else:
        for root, dirs, files in os.walk(input_):
            for file in files:
                if file.endswith(".txt"):
                    fp = os.path.join(root, file)
                    process_file(fp)


# -------------------------------------------------- CLI -------------------------------------------------- #

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Perform tokenization on the raw linguistic data.')
    parser.add_argument('--input', '--i', type=str, help='Directory or txt file', required=True)
    parser.add_argument('--ngrams', '--n', type=int, help='Generate n-grams', default=1)
    parser.add_argument('--chars', '--c', action=argparse.BooleanOptionalAction, help='Use characters instead of words',
                        default=False)

    args = parser.parse_args()

    input_ = args.input
    ngrams_ = args.ngrams
    chars = args.chars

    tweet_tokenizer = TweetTokenizer()

    main()

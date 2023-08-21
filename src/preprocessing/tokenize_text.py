"""
:author: Siméon FEREZ
:version: 1.0.0
:copyright: Copyright © 2023 by Siméon FEREZ. All rights reserved. This work may not be reproduced, in whole or in part, without the written permission of the author.
:description: Tokenize the raw linguistic data txt files.

CLI Arguments:
    - --input, --i: Directory or txt file
    - --ngrams, --n: Generate n-grams (default: 1)
    - --chars, --c: Use characters instead of words (default: False)

Examples:
    >>> python tokenize_text.py --input data.txt
    >>> python tokenize_text.py --input data.txt --ngrams 2
    >>> python tokenize_text.py --input data.txt --ngrams 2 --chars
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
    """
    Generate n-grams from a list of tokens.

    :param tokens: list of tokens
    :type tokens: list
    :param n: n-gram
    :type n: int
    :return: list of n-grams
    :rtype: list

    >>> generate_ngrams(['I', 'am', 'so', 'happy'], 2)
    >>> ['I am', 'am so', 'so happy']
    """
    n_grams = ngrams(tokens, n)
    return [" ".join(gram) for gram in n_grams]


def process_file(fp):
    """
    Process a txt file by tokenizing it.

    :param fp: file path
    :type fp: str
    :return: None
    :rtype: None

    >>> process_file('data.txt')
    """
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
    """
    Main function of the tokenize_text.py script.

    :return: None
    :rtype: None

    >>> main()
    """
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
    """
    Command Line Interface of the tokenize_text.py script.
    
    Args:
        --input, --i: Directory or txt file
        --ngrams, --n: Generate n-grams (default: 1)
        --chars, --c: Use characters instead of words (default: False)
        
    Examples:
        >>> python tokenize_text.py --input data.txt
        >>> python tokenize_text.py --input data.txt --ngrams 2
        >>> python tokenize_text.py --input data.txt --ngrams 2 --chars
    """
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

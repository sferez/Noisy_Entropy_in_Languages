"""
:author: Siméon FEREZ
:version: 1.0.0
:copyright: Copyright © 2023 by Siméon FEREZ. All rights reserved. This work may not be reproduced, in whole or in part, without the written permission of the author.
:description: Run the full analysis of the entropy estimation project, including unigram entropy estimation, PPM entropy estimation, and Hrate entropy estimation.

CLI Arguments:
    - --tokens, --t: Path to list of tokens
    - --vocab, --v: Path to vocabulary file, if not provided, all tokens will be considered as vocabulary
    - --use_vocab, --uv: Whether to use vocabulary for unigram entropy estimation (default: False)
    - --unigrams, --u: Skip unigram entropy estimation
    - --ppm, --p: Skip PPM entropy estimation
    - --hrate, --h: Skip Hrate entropy estimation
    - --fast, --f: Skip PPM entropy estimation, and uncertainty analysis
    - --output_dir, --o: Path to output directory (default: results/<file_name>)

Examples:
    >>> python3 src/entropyEstimation/full_analysis.py --tokens tokens.txt --vocab vocab.txt
    >>> python3 src/entropyEstimation/full_analysis.py --tokens tokens.txt --vocab vocab.txt  --fast
    >>> python3 src/entropyEstimation/full_analysis.py --tokens tokens.txt --vocab vocab.txt  --unigrams
"""

# ------------------------------------------------ IMPORTS ------------------------------------------------ #

# External
import argparse
import os

# ----------------------------------------------- CONSTANTS ----------------------------------------------- #

unigram_max_tokens = [None, 25_000, 50_000, 100_000]
unigram_max_tokens_fast = [150_000, 200_000, 250_000]
ppm_max_train = [10_000]
hrate_max_tokens = [100_000]


# ----------------------------------------------- FUNCTIONS ----------------------------------------------- #

def run_unigram_entropy(tokens, vocab):
    """
    Run the unigram entropy estimation for the given tokens and vocabulary.

    :param tokens: tokens file
    :type tokens: str
    :param vocab: vocab file
    :type vocab: str
    :return: None
    :rtype: None

    >>> run_unigram_entropy('tokens.txt', 'vocab.txt')
    """
    print('Estimating unigram entropy...')
    for max_tokens in unigram_max_tokens:
        print(f'  max_tokens: {max_tokens}')
        os.system(
            f'python3 src/entropyEstimation/entropy.py --tokens {tokens} {"--vocab " + vocab if use_vocab else ""} {"--max_tokens " + str(max_tokens) if max_tokens else ""} {"--b" if not fast else ""} {"--o " + output_dir if output_dir else ""}')

    for max_tokens in unigram_max_tokens_fast:
        print(f'  max_tokens: {max_tokens}')
        os.system(
            f'python3 src/entropyEstimation/entropy.py --tokens {tokens} {"--vocab " + vocab if use_vocab else ""} {"--max_tokens " + str(max_tokens) if max_tokens else ""} {"--o " + output_dir if output_dir else ""}')


def run_ppm_entropy(tokens, vocab):
    """
    Run the PPM entropy estimation for the given tokens and vocabulary.

    :param tokens: tokens file
    :type tokens: str
    :param vocab: vocab file
    :type vocab: str
    :return: None
    :rtype: None

    >>> run_ppm_entropy('tokens.txt', 'vocab.txt')
    """
    tokens_ = tokens.replace('.txt', '_ppm.txt')
    print('Estimating PPM entropy...')
    print('  Decay: None')
    for max_train in ppm_max_train:
        print(f'    max_train: {max_train}')
        os.system(f'python3 src/entropyEstimation/ppm.py --tokens {tokens_} --vocab {vocab} --max_train {max_train} {"--o " + output_dir if output_dir else ""}')
    print('  Decay: True')
    for max_train in ppm_max_train:
        print(f'    max_train: {max_train}')
        os.system(
            f'python3 src/entropyEstimation/ppm.py --tokens {tokens_} --vocab {vocab} --max_train {max_train} --d {"--o " + output_dir if output_dir else ""}')


def run_hrate_entropy(tokens):
    """
    Run the Hrate entropy estimation for the given tokens.

    :param tokens: tokens file
    :type tokens: str
    :return: None
    :rtype: None

    >>> run_hrate_entropy('tokens.txt')
    """
    print('Estimating Hrate entropy...')
    for max_tokens in hrate_max_tokens:
        print(f'  max_tokens: {max_tokens}')
        os.system(f'python3 src/entropyEstimation/Hrate.py --tokens {tokens} --max_tokens {max_tokens} {"--o " + output_dir if output_dir else ""} {"--f" if fast else ""}')


# ------------------------------------------------- MAIN ------------------------------------------------- #

def main():
    """
    Main function of full_analysis.py

    :return: None
    :rtype: None

    >>> main()
    """
    print('Running full analysis...')
    if not skip_unigrams:
        run_unigram_entropy(tokens, vocab)
    if not skip_ppm:
        run_ppm_entropy(tokens, vocab)
    if not skip_hrate:
        run_hrate_entropy(tokens)


# -------------------------------------------------- CLI -------------------------------------------------- #

if __name__ == '__main__':
    """
    Command Line Interface of full_analysis.py
    
    Args:
        --tokens, --t: Path to list of tokens
        --vocab, --v: Path to vocabulary file, if not provided, all tokens will be considered as vocabulary
        --use_vocab, --uv: Whether to use vocabulary for unigram entropy estimation (default: False)
        --unigrams, --u: Skip unigram entropy estimation
        --ppm, --p: Skip PPM entropy estimation
        --hrate, --h: Skip Hrate entropy estimation
        --fast, --f: Skip PPM entropy estimation, and uncertainty analysis 
        --output_dir, --o: Path to output directory (default: results/<file_name>)
        
    Examples:
        >>> python3 src/entropyEstimation/full_analysis.py --tokens tokens.txt --vocab vocab.txt
        >>> python3 src/entropyEstimation/full_analysis.py --tokens tokens.txt --vocab vocab.txt  --fast
        >>> python3 src/entropyEstimation/full_analysis.py --tokens tokens.txt --vocab vocab.txt  --unigrams
    """
    parser = argparse.ArgumentParser(description='Run the full analysis of the entropy estimation project.')
    parser.add_argument('--tokens', '--t', type=str, help='Path to list of tokens')
    parser.add_argument('--vocab', '--v', type=str, help='Path to vocabulary')
    parser.add_argument('--use_vocab', '--uv', type=int, action=argparse.BooleanOptionalAction, default=False,
                        help='Use vocab for unigram entropy estimation')
    parser.add_argument('--unigrams', '--u', type=int, action=argparse.BooleanOptionalAction,
                        help='Skip unigram entropy estimation', default=False)
    parser.add_argument('--ppm', '--p', type=int, action=argparse.BooleanOptionalAction,
                        help='Skip PPM entropy estimation', default=False)
    parser.add_argument('--hrate', '--h', type=int, action=argparse.BooleanOptionalAction,
                        help='Skip Hrate entropy estimation', default=False)
    parser.add_argument('--fast', '--f', type=int, action=argparse.BooleanOptionalAction,
                        help='Skip PPM entropy estimation, and uncertainty analysis', default=False)
    parser.add_argument('--output_dir', '--o', type=str, help='Path to output directory', default=None, required=False)

    args = parser.parse_args()
    tokens = args.tokens
    vocab = args.vocab
    use_vocab = args.use_vocab
    skip_unigrams = args.unigrams
    skip_ppm = args.ppm
    skip_hrate = args.hrate
    fast = args.fast
    output_dir = args.output_dir

    if fast:
        skip_ppm = True

    main()

"""
Run the full analysis of the entropy estimation project.
"""

# ------------------------------------------------ IMPORTS ------------------------------------------------ #

# External
import argparse
import os

# ----------------------------------------------- CONSTANTS ----------------------------------------------- #

unigram_max_tokens = [None, 25_000, 50_000, 100_000]
unigram_max_tokens_fast = [150_000, 200_000, 250_000]
ppm_max_train = [10_000]
hrate_max_tokens = [150_000]


# ----------------------------------------------- FUNCTIONS ----------------------------------------------- #

def run_unigram_entropy(tokens, vocab):
    print('Estimating unigram entropy...')
    for max_tokens in unigram_max_tokens:
        print(f'  max_tokens: {max_tokens}')
        os.system(
            f'python3 src/entropyEstimation/entropy.py --tokens {tokens} {"--vocab " + vocab if use_vocab else ""} {"--max_tokens " + str(max_tokens) if max_tokens else ""} {"--b" if not fast else ""}')

    for max_tokens in unigram_max_tokens_fast:
        print(f'  max_tokens: {max_tokens}')
        os.system(
            f'python3 src/entropyEstimation/entropy.py --tokens {tokens} {"--vocab " + vocab if use_vocab else ""} {"--max_tokens " + str(max_tokens) if max_tokens else ""}')


def run_ppm_entropy(tokens, vocab):
    tokens_ = tokens.replace('.txt', '_ppm.txt')
    print('Estimating PPM entropy...')
    print('  Decay: None')
    for max_train in ppm_max_train:
        print(f'    max_train: {max_train}')
        os.system(f'python3 src/entropyEstimation/ppm.py --tokens {tokens_} --vocab {vocab} --max_train {max_train}')
    print('  Decay: True')
    for max_train in ppm_max_train:
        print(f'    max_train: {max_train}')
        os.system(
            f'python3 src/entropyEstimation/ppm.py --tokens {tokens_} --vocab {vocab} --max_train {max_train} --d')


def run_hrate_entropy(tokens):
    print('Estimating Hrate entropy...')
    for max_tokens in hrate_max_tokens:
        print(f'  max_tokens: {max_tokens}')
        os.system(f'python3 src/entropyEstimation/Hrate.py --tokens {tokens} --max_tokens {max_tokens}')


# ------------------------------------------------- MAIN ------------------------------------------------- #

def main():
    print('Running full analysis...')
    if not skip_unigrams:
        run_unigram_entropy(tokens, vocab)
    if not skip_ppm:
        run_ppm_entropy(tokens, vocab)
    if not skip_hrate:
        run_hrate_entropy(tokens)


# -------------------------------------------------- CLI -------------------------------------------------- #

if __name__ == '__main__':
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

    args = parser.parse_args()
    tokens = args.tokens
    vocab = args.vocab
    use_vocab = args.use_vocab
    skip_unigrams = args.unigrams
    skip_ppm = args.ppm
    skip_hrate = args.hrate
    fast = args.fast

    if fast:
        skip_ppm = True

    main()

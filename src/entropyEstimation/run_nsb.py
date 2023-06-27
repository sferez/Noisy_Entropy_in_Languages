"""
This script calculates the entropy of a given vocabulary using the NSB method.
"""

# ------------------------------------------------ IMPORTS ------------------------------------------------ #

# External
from collections import Counter
import numpy as np
import argparse
import os
from nsb import make_nxkx, S, dS


# ----------------------------------------------- FUNCTIONS ----------------------------------------------- #


def process_file():
    global vocab
    with open(tokens, 'r') as f:
        all_tokens = f.read().splitlines()  # Assuming each line in vocab.txt is a separate token.
    counts = Counter(all_tokens)
    if vocab:
        print(f'Vocab file provided: {vocab}')
        i=0
        with open(vocab, 'r') as f:
            vocab = set(f.read().splitlines())
            for token in vocab:
                if token not in counts:
                    i += 1
                    counts[token] = 0
        print(f'Vocab size: {len(vocab)}, Number of OOV tokens: {i}')
    return counts, all_tokens


def nsb_entropy(counts):
    histogram = list(counts.values())
    nxkx = make_nxkx(np.array(histogram), len(histogram))
    entropy = S(nxkx, sum(histogram), len(histogram))
    ds = dS(nxkx, sum(histogram), len(histogram))

    std = np.sqrt(abs(ds - entropy ** 2))
    # get entropy in bits
    entropy /= np.log(2)
    ds /= np.log(2)
    std /= np.log(2)

    return entropy, std


# ------------------------------------------------- MAIN ------------------------------------------------- #

def main():
    counts, all_tokens = process_file()

    entropy, std = nsb_entropy(counts)

    print(f'Entropy: {round(entropy,4)}')
    print(f'Std_Dev: {round(std,4)}')
    print(f'Confidence Interval (95%): [{round(entropy - std,4)}, {round(entropy + std,4)}]')


# -------------------------------------------------- CLI -------------------------------------------------- #

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate the nsb entropy of a given vocabulary.')
    parser.add_argument('--tokens', '--t', type=str, help='Path to list of tokens')
    parser.add_argument('--vocab', '--v', type=str, help='Path to vocabulary file', default=None)

    args = parser.parse_args()
    tokens = args.tokens
    vocab = args.vocab

    main()

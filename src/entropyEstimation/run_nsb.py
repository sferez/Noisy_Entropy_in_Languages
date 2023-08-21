"""
:author: Siméon FEREZ
:version: 1.0.0
:copyright: Copyright © 2023 by Siméon FEREZ. All rights reserved. This work may not be reproduced, in whole or in part, without the written permission of the author.
:description: Run the NSB entropy estimation for the given tokens and vocabulary.

CLI Arguments:
    - --tokens, --t: Path to list of tokens
    - --vocab, --v: Path to list of vocabulary

Examples:
    >>> python3 src/entropyEstimation/nsb.py --tokens tokens.txt
    >>> python3 src/entropyEstimation/nsb.py --tokens tokens.txt --vocab vocab.txt

"""

# ------------------------------------------------ IMPORTS ------------------------------------------------ #

# External
from collections import Counter
import numpy as np
import argparse
from nsb import make_nxkx, S, dS


# ----------------------------------------------- FUNCTIONS ----------------------------------------------- #


def process_file():
    """
    Process the file containing the tokens and return the counts of each token and the list of all tokens.

    :return: counts, all_tokens
    :rtype: Counter, list

    >>> process_file()
    """
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
    """
    Calculate the nsb entropy of the given counts.

    :param counts: counts of each token
    :type counts: Counter
    :return: entropy, std
    :rtype: float, float

    >>> nsb_entropy(Counter(['a', 'a', 'b', 'b', 'b']))
    """
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
    """
    Main function of nsb.py

    :return: None
    :rtype: None

    >>> main()
    """
    counts, all_tokens = process_file()

    entropy, std = nsb_entropy(counts)

    print(f'Entropy: {round(entropy,4)}')
    print(f'Std_Dev: {round(std,4)}')
    print(f'Confidence Interval (95%): [{round(entropy - std,4)}, {round(entropy + std,4)}]')


# -------------------------------------------------- CLI -------------------------------------------------- #

if __name__ == '__main__':
    """
    Command Line Interface of nsb.py
    
    Args:
        --tokens, --t: Path to list of tokens
        --vocab, --v: Path to list of vocabulary
            
    Examples:
        >>> python3 src/entropyEstimation/nsb.py --tokens tokens.txt
        >>> python3 src/entropyEstimation/nsb.py --tokens tokens.txt --vocab vocab.txt
    """
    parser = argparse.ArgumentParser(description='Calculate the nsb entropy of a given vocabulary.')
    parser.add_argument('--tokens', '--t', type=str, help='Path to list of tokens')
    parser.add_argument('--vocab', '--v', type=str, help='Path to vocabulary file', default=None)

    args = parser.parse_args()
    tokens = args.tokens
    vocab = args.vocab

    main()

"""
:author: Siméon FEREZ
:version: 1.0.0
:copyright: Copyright © 2023 by Siméon FEREZ. All rights reserved. This work may not be reproduced, in whole or in part, without the written permission of the author.
:description: Use Plug-in entropy estimation to estimate the entropy of a given distribution of tokens.

CLI Arguments:
    - --tokens, --t: Path to list of tokens
    - --vocab, --v: Path to vocabulary file, if not provided, all tokens will be considered as vocabulary
    - --max_tokens, --mt: Maximum number of tokens to consider
    - --bootstrap, --b: Whether to perform bootstrap analysis
    - --output_dir, --o: Path to output directory

Examples:
    >>> python3 src/entropyEstimation/entropy.py --tokens tokens.txt --vocab vocab.txt
    >>> python3 src/entropyEstimation/entropy.py --tokens tokens.txt --max_tokens 1000 --bootstrap
"""

# ------------------------------------------------ IMPORTS ------------------------------------------------ #

# External
from collections import Counter
import gc
import argparse
import os
import pandas as pd

# Internal
from src.entropyEstimation.run_nsb import nsb_entropy


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
        i = 0
        with open(vocab, 'r') as f:
            vocab = set(f.read().splitlines())
            for token in vocab:
                if token not in counts:
                    i += 1
                    counts[token] = 0
        print(f'Vocab size: {len(vocab)}, Number of OOV tokens: {i}')
    return counts, all_tokens


# ------------------------------------------------- MAIN ------------------------------------------------- #

def main():
    """
    Main function of entropy.py

    :return: None
    :rtype: None

    >>> main()
    """
    if output_dir:
        result_dir = f'results/{output_dir}/unigrams'
    else:
        result_dir = f'results/{tokens.split("/")[-1].split(".")[0]}/unigrams'  # results/<file_name>/unigrams
    os.makedirs(result_dir, exist_ok=True)

    os.system(
        f'Rscript src/entropyEstimation/entropy.R --tokens {tokens}  --output_dir {result_dir} {"--vocab " + vocab if vocab else ""} {"--max_tokens " + str(max_tokens) if max_tokens else ""} {"--bootstrap 1" if bootstrap else ""}')

    print('Method: NSB')
    counts, all_tokens = process_file()
    del all_tokens
    gc.collect()
    nsb_e, nsb_std = nsb_entropy(counts)
    print(
        f'Original Entropy: {round(nsb_e, 3)}\n'
        f'SD: {round(nsb_std, 3)}\n'
        f'95% CI: [{round(nsb_e - nsb_std, 3)} {round(nsb_e + nsb_std, 3)}]')
    if bootstrap:
        df = pd.DataFrame([[tokens, 'NSB', nsb_e, 0, 0, nsb_std, [nsb_e - nsb_std, nsb_e + nsb_std]]],
                          columns=['file', 'method', 'entropy', 'mae', 'mse', 'sd', 'ci'])
    else:
        df = pd.DataFrame([[tokens, 'NSB', nsb_e]],
                          columns=['file', 'method', 'entropy'])
    file = f'{result_dir}/unigrams{"_" + str(max_tokens) if max_tokens else ""}.csv'
    df2 = pd.read_csv(file)
    df = pd.concat([df, df2])
    df.to_csv(file, index=False)


# -------------------------------------------------- CLI -------------------------------------------------- #

if __name__ == '__main__':
    """
    Command Line Interface for entropy.py
    
    Args:
        --tokens, --t: Path to list of tokens
        --vocab, --v: Path to vocabulary file, if not provided, all tokens will be considered as vocabulary
        --max_tokens, --mt: Maximum number of tokens to consider
        --bootstrap, --b: Whether to perform bootstrap analysis
        --output_dir, --o: Path to output directory
        
    Examples:
        >>> python3 src/entropyEstimation/entropy.py --tokens tokens.txt --vocab vocab.txt
        >>> python3 src/entropyEstimation/entropy.py --tokens tokens.txt --max_tokens 1000 --bootstrap
    """
    parser = argparse.ArgumentParser(description='Calculate the entropy of a given vocabulary.')
    parser.add_argument('--tokens', '--t', type=str, help='Path to list of tokens')
    parser.add_argument('--vocab', '--v', type=str,
                        help='Path to vocabulary file, if not provided, all tokens will be considered as vocabulary',
                        default=None)
    parser.add_argument('--max_tokens', '--mt', type=int, help='Maximum number of tokens to consider', default=None)
    parser.add_argument('--bootstrap', '--b', type=int, action=argparse.BooleanOptionalAction,
                        help='Whether to perform bootstrap analysis', default=False)
    parser.add_argument('--output_dir', '--o', type=str, help='Path to output directory', default=None, required=False)

    args = parser.parse_args()
    tokens = args.tokens
    vocab = args.vocab
    max_tokens = args.max_tokens
    bootstrap = args.bootstrap
    output_dir = args.output_dir

    main()

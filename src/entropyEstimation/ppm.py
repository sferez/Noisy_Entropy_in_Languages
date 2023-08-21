"""
:author: Siméon FEREZ
:version: 1.0.0
:copyright: Copyright © 2023 by Siméon FEREZ. All rights reserved. This work may not be reproduced, in whole or in part, without the written permission of the author.
:description: Use PPM entropy estimation to estimate the entropy of a given corpus.

CLI Arguments:
    - --tokens: Path to list of tokens
    - --vocab: Path to list of vocabulary
    - --max_train: Maximum number of training samples to consider
    - --decay: Whether to use the decay version of the algorithm
    - --output_dir: Path to output directory

Examples:
    >>> python3 src/entropyEstimation/ppm.py --tokens tokens.txt --vocab vocab.txt
    >>> python3 src/entropyEstimation/ppm.py --tokens tokens.txt --vocab vocab.txt --decay
    >>> python3 src/entropyEstimation/ppm.py --tokens tokens.txt --vocab vocab.txt --max_train 5000
"""

# ------------------------------------------------ IMPORTS ------------------------------------------------ #

# External
import argparse
import os


# ------------------------------------------------- MAIN ------------------------------------------------- #
def main():
    """
    Main function of ppm.py

    :return: None
    :rtype: None

    >>> main()
    """
    if output_dir:
        result_dir = f'results/{output_dir}/ppm'
    else:
        result_dir = f'results/{os.path.basename(tokens).split(".")[0].replace("_ppm", "")}/ppm'
    os.makedirs(result_dir, exist_ok=True)

    os.system(
        f'Rscript src/entropyEstimation/ppm.R --tokens {tokens} --vocab {vocab} --output_dir {result_dir}  {"--max_train " + str(max_train) if max_train else ""} {"--decay 1" if decay else ""}')


# -------------------------------------------------- CLI -------------------------------------------------- #

if __name__ == '__main__':
    """
    Command Line Interface of ppm.py
    
    Args:
        --tokens: Path to list of tokens
        --vocab: Path to list of vocabulary
        --max_train: Maximum number of training samples to consider
        --decay: Whether to use the decay version of the algorithm
        --output_dir: Path to output directory
        
    Examples:
        >>> python3 src/entropyEstimation/ppm.py --tokens tokens.txt --vocab vocab.txt
        >>> python3 src/entropyEstimation/ppm.py --tokens tokens.txt --vocab vocab.txt --decay
        >>> python3 src/entropyEstimation/ppm.py --tokens tokens.txt --vocab vocab.txt --max_train 5000 
    """
    parser = argparse.ArgumentParser(description='Calculate the entropy of a given vocabulary.')
    parser.add_argument('--tokens', '--t', type=str, help='Path to list of tokens')
    parser.add_argument('--vocab', '--v', type=str, help='Path to list of vocabulary')
    parser.add_argument('--max_train', '--mt', type=int, help='Maximum number of training samples to consider',
                        default=None)
    parser.add_argument('--decay', '--d', type=int, action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument('--output_dir', '--o', type=str, help='Path to output directory', default=None, required=False)

    args = parser.parse_args()
    tokens = args.tokens
    vocab = args.vocab
    max_train = args.max_train
    decay = args.decay
    output_dir = args.output_dir

    main()

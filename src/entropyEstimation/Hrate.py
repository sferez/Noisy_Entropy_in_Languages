"""
:author: Siméon FEREZ
:version: 1.0.0
:copyright: Copyright © 2023 by Siméon FEREZ. All rights reserved. This work may not be reproduced, in whole or in part, without the written permission of the author.
:description: Use Entropy Rate estimation to estimate the entropy of a given corpus.

CLI Arguments:
    - --tokens: Path to list of tokens
    - --max_tokens: Maximum number of tokens to consider
    - --fast: Whether to use the fast version of the algorithm
    - --output_dir: Path to output directory

Examples:
    >>> python3 src/entropyEstimation/Hrate.py --tokens tokens.txt
    >>> python3 src/entropyEstimation/Hrate.py --tokens tokens.txt --max_tokens 100000
"""

# ------------------------------------------------ IMPORTS ------------------------------------------------ #

# External
import argparse
import os


# ------------------------------------------------- MAIN ------------------------------------------------- #
def main():
    """
    Main function of Hrate.py

    :return: None
    :rtype: None

    >>> main()
    """
    if output_dir:
        result_dir = f'results/{output_dir}/Hrate'
    else:
        result_dir = f'results/{os.path.basename(tokens).split(".")[0]}/Hrate'
    os.makedirs(result_dir, exist_ok=True)

    os.system(
        f'Rscript src/entropyEstimation/Hrate.R --tokens {tokens} --output_dir {result_dir} --max_tokens {str(max_tokens) if max_tokens else "0"} {"--fast 1" if fast else ""}')


# -------------------------------------------------- CLI -------------------------------------------------- #

if __name__ == '__main__':
    """
    Command Line Interface of Hrate.py
    
    Args:
        --tokens: Path to list of tokens
        --max_tokens: Maximum number of tokens to consider
        --fast: Whether to use the fast version of the algorithm
        --output_dir: Path to output directory
        
    Examples:
        >>> python3 src/entropyEstimation/Hrate.py --tokens tokens.txt
        >>> python3 src/entropyEstimation/Hrate.py --tokens tokens.txt --max_tokens 100000
    """
    parser = argparse.ArgumentParser(description='Calculate the entropy of a given vocabulary.')
    parser.add_argument('--tokens', '--t', type=str, help='Path to list of tokens')
    parser.add_argument('--max_tokens', '--mt', type=int, help='Maximum number of tokens to consider', default=None)
    parser.add_argument('--fast', '--f', type=int, action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument('--output_dir', '--o', type=str, help='Path to output directory', default=None, required=False)

    args = parser.parse_args()
    tokens = args.tokens
    max_tokens = args.max_tokens
    fast = args.fast
    output_dir = args.output_dir

    main()

"""
This script calculates the entropy of a given vocabulary.
"""

# ------------------------------------------------ IMPORTS ------------------------------------------------ #

# External
import argparse
import os


# ------------------------------------------------- MAIN ------------------------------------------------- #
def main():
    os.makedirs(f'results/{os.path.basename(tokens)}', exist_ok=True)
    result_dir = f'results/{os.path.basename(tokens)}'

    os.system(
        f'Rscript src/entropyEstimation/Hrate.R --tokens {tokens} --output_dir {result_dir} --max_tokens {str(max_tokens) if max_tokens else "0"} {"--fast 1" if fast else ""}')


# -------------------------------------------------- CLI -------------------------------------------------- #

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate the entropy of a given vocabulary.')
    parser.add_argument('--tokens', '--t', type=str, help='Path to list of tokens')
    parser.add_argument('--max_tokens', '--mt', type=int, help='Maximum number of tokens to consider', default=None)
    parser.add_argument('--fast', '--f', type=int, action=argparse.BooleanOptionalAction, default=False)

    args = parser.parse_args()
    tokens = args.tokens
    max_tokens = args.max_tokens
    fast = args.fast

    main()

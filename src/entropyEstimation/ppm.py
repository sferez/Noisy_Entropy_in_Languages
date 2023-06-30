"""
This script calculates the entropy of a given vocabulary.
"""

# ------------------------------------------------ IMPORTS ------------------------------------------------ #

# External
import argparse
import os


# ------------------------------------------------- MAIN ------------------------------------------------- #
def main():
    result_dir = f'results/{os.path.basename(tokens).split(".")[0].replace("ppm", "")}'
    os.makedirs(result_dir, exist_ok=True)

    os.system(
        f'Rscript src/entropyEstimation/ppm.R --tokens {tokens} --vocab {vocab} --output_dir {result_dir}  {"--max_train " + str(max_train) if max_train else ""} {"--decay 1" if decay else ""}')


# -------------------------------------------------- CLI -------------------------------------------------- #

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate the entropy of a given vocabulary.')
    parser.add_argument('--tokens', '--t', type=str, help='Path to list of tokens')
    parser.add_argument('--vocab', '--v', type=str, help='Path to list of vocabulary')
    parser.add_argument('--max_train', '--mt', type=int, help='Maximum number of training samples to consider',
                        default=None)
    parser.add_argument('--decay', '--d', type=int, action=argparse.BooleanOptionalAction, default=False)

    args = parser.parse_args()
    tokens = args.tokens
    vocab = args.vocab
    max_train = args.max_train
    decay = args.decay

    main()

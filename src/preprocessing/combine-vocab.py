"""
Combine all vocab files into one
"""

# ---------------------------------------------------- IMPORTS ------------------------------------------------------- #

# External
import argparse
import os
import pandas as pd
from tqdm import tqdm

# --------------------------------------------------- CONSTANT ------------------------------------------------------- #

vocab = set()


# ---------------------------------------------------- SCRIPT -------------------------------------------------------- #


def main():
    global i
    full_paths = []
    for root, dirs, files in os.walk(input_):
        for file in files:
            if file.endswith(".txt") and 'vocab' in file and not file.endswith("combined.txt"):
                full_paths.append(os.path.join(root, file))

    for fp in full_paths:
        with open(fp, 'r') as f:
            for line in f:
                vocab.add(line.strip())
                i += 1
            f.close()

    with open(os.path.join(input_, output), 'w') as f:
        for token in vocab:
            f.write(f'{token}\n')
        f.close()

    print(f'Combined {i} vocabs into {len(vocab)} tokens in {output}.')

    print('COMBINED VOCAB FILES:')
    for fp in full_paths:
        print(fp.split('/')[-1])

# ---------------------------------------------------- MAIN ---------------------------------------------------------- #

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Combine CSV files')

    parser.add_argument('--input', '--i', type=str, help='Directory', required=True)
    parser.add_argument('--output', '--o', type=str, help='Final file name (Default: vocab-combined.txt)',
                        default='vocab-combined.txt')

    args = parser.parse_args()

    input_ = args.input
    output = args.output
    i = 0

    main()

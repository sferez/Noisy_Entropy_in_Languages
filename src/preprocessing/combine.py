"""
Combine all the data into one file from a directory
"""

# ---------------------------------------------------- IMPORTS ------------------------------------------------------- #

# External
import argparse
import os
import pandas as pd


# ---------------------------------------------------- SCRIPT -------------------------------------------------------- #

def main():
    full_paths = []
    for root, dirs, files in os.walk(input_):
        for file in files:
            if file.endswith(".csv"):
                full_paths.append(os.path.join(root, file))

    dfs = [pd.read_csv(fp) for fp in full_paths]

    df = pd.concat(dfs, ignore_index=True)
    df.to_csv(os.path.join(input_, output), index=False)

    print('COMBINED CSV FILES:')
    for fp in full_paths:
        print(fp.split('/')[-1])


# ---------------------------------------------------- MAIN ---------------------------------------------------------- #

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Combine CSV files')

    parser.add_argument('--input', '--i', type=str, help='Directory', required=True)
    parser.add_argument('--output', '--o', type=str, help='Final file name (Default: combined.csv)', default='combined.csv')

    args = parser.parse_args()

    input_ = args.input
    output = args.output

    main()

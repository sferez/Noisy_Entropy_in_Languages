"""
Perform data cleaning on the raw linguistic data (tweets).
"""

# -------------------------------------------------- IMPORTS -------------------------------------------------- #

# External
import pandas as pd
import argparse


# ------------------------------------------------- MAIN ------------------------------------------------- #

def main():
    df = pd.read_csv(input_file)
    df['class'] = class_
    df.to_csv(input_file, index=False)


# -------------------------------------------------- CLI -------------------------------------------------- #

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Perform data cleaning on the raw linguistic data.')
    parser.add_argument('--input_file', '--i', type=str, help='Directory containing the raw data.', required=True)
    parser.add_argument('--class_', '--c', type=str, help='Class to labelled the data', required=True)

    args = parser.parse_args()

    input_file = args.input_file
    class_ = args.class_

    main()

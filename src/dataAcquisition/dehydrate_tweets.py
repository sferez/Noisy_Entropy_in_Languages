"""
:author: Siméon FEREZ
:version: 1.0.0
:copyright: Copyright © 2023 by Siméon FEREZ. All rights reserved. This work may not be reproduced, in whole or in part, without the written permission of the author.
:description: Dehydrate tweets from a csv file by keeping only tweet_id

CLI Arguments:
    - --input, --i: Directory or CSV file
    - --output, --o: Directory where you want the dehydrated CSV files

Example:
    >>> python dehydrate_tweets.py --input data.csv --output dehydrated/
"""

# ------------------------------------------- IMPORTS ------------------------------------------- #

# External
import os
import pandas as pd
from pathlib import Path
import argparse


# ------------------------------------------- FUNCTIONS ------------------------------------------- #


def process_file(fp):
    """
    Process a csv file with tweet_id and dehydrate it

    :param fp: File path
    :type fp: str
    :return: None
    :rtype: None

    >>> process_file('data.csv')
    """
    df = pd.read_csv(fp)
    tweet_id_df = df[['tweet_id']].dropna().astype(int)
    tweet_id_df.to_csv(fp, index=False)

    print(f'Dehydrated {fp}')
    return tweet_id_df


# ---------------------------------------------- MAIN ---------------------------------------------- #

def main():
    """
    Main function of dehydrate_tweets.py

    :return: None
    :rtype: None

    >>> main()
    """
    if os.path.isfile(input_):  # Single file
        fp = input_
        tweet_id_df = process_file(fp)

        new_dir = os.path.join(output + "_dehydrated")
        os.makedirs(new_dir, exist_ok=True)

        tweet_id_df.to_csv(os.path.join(new_dir, Path(fp).name), index=False)
    else:
        for root, dirs, files in os.walk(input_):
            for file in files:
                if file.endswith(".csv"):
                    fp = os.path.join(root, file)
                    tweet_id_df = process_file(fp)

                    # Replicate the directory structure in output directory
                    rel_path = os.path.relpath(root, input_)
                    new_dir = os.path.join(output, rel_path + "_dehydrated")
                    os.makedirs(new_dir, exist_ok=True)

                    tweet_id_df.to_csv(os.path.join(new_dir, file), index=False)


# ------------------------------------------- MAIN ------------------------------------------- #

if __name__ == '__main__':
    """
    Command line arguments of dehydrate_tweets.py
    
    Args:
        --input, --i: Directory or CSV file
        --output, --o: Directory where you want the dehydrated CSV files
        
    Example:
        >>> python dehydrate_tweets.py --input data.csv --output dehydrated/
    """
    parser = argparse.ArgumentParser(description='Dehydrate tweets from a csv file by keeping only tweet_id')

    parser.add_argument('--input', '--i', type=str, help='Directory or CSV file', required=True)
    parser.add_argument('--output', '--o', type=str, help='Directory where you want the dehydrated CSV files',
                        required=True)

    args = parser.parse_args()
    input_ = args.input
    output = args.output

    main()

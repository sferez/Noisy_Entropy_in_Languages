"""
This script takes a directory containing CSV files and dehydrates them by keeping only the tweet_id column.
"""

# ------------------------------------------- IMPORTS ------------------------------------------- #

# External
import os
import pandas as pd
from pathlib import Path
import argparse


# ------------------------------------------- FUNCTIONS ------------------------------------------- #

def dehydrate_csv_files(directory_path, output_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".csv"):
                df = pd.read_csv(os.path.join(root, file))
                tweet_id_df = df[['tweet_id']].dropna().astype('int64')

                # Replicate the directory structure in output directory
                rel_path = os.path.relpath(root, directory_path)
                new_dir = os.path.join(output_path, rel_path + "_dehydrated")
                os.makedirs(new_dir, exist_ok=True)

                tweet_id_df.to_csv(os.path.join(new_dir, file), index=False)


# ------------------------------------------- MAIN ------------------------------------------- #

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Dehydrate tweets from a csv file by keeping only tweet_id')

    parser.add_argument('--input_dir', '--i', type=str, help='Directory containing the CSV files', required=True)
    parser.add_argument('--output_dir', '--o', type=str, help='Directory where you want the dehydrated CSV files',
                        required=False)

    args = parser.parse_args()
    input_dir = args.input_dir
    output_dir = args.output_dir

    dehydrate_csv_files(input_dir, output_dir)

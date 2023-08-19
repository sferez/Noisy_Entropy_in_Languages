"""
:author: Siméon FEREZ
:version: 1.0.0
:copyright: Copyright © 2023 by Siméon FEREZ. All rights reserved. This work may not be reproduced, in whole or in part, without the written permission of the author.

Combine metadata for a Twitter CSV file.
"""

# -------------------------------------------------- IMPORTS -------------------------------------------------- #

# External
import pandas as pd
import argparse


# ------------------------------------------------- MAIN ------------------------------------------------- #

def main():
    """
    Main function, combines metadata for a Twitter CSV file.
    :return: None
    :rtype: None
    >>> main()
    """
    print('Combine metadata...')

    # Read CSV files
    df_text = pd.read_csv(text)
    df_metadata = pd.read_csv(metadata)
    df_text = df_text[['tweet_id', 'text']]

    # Combine CSV files
    df = pd.concat([df_text, df_metadata], axis=1)

    l = len(df)
    df.dropna(inplace=True)
    print(f'Dropped {l - len(df)} rows')

    # Save CSV file
    df.to_csv(text, index=False)
    print(f'Saved {text}')


# -------------------------------------------------- CLI -------------------------------------------------- #

if __name__ == '__main__':
    """
    Command Line Interface of the combine metadata script.
    
    Args:
        --text, --t: CSV file with text
        --metadata, --m: CSV file with metadata
        
    Examples:
        >>> python combine-metadata.py --text data/combined.csv --metadata data/metadata.csv
    """
    parser = argparse.ArgumentParser(description='Generate metadata for a CSV file.')
    parser.add_argument('--text', '--t', type=str, help='CSV file with text', required=True)
    parser.add_argument('--metadata', '--m', type=str, help='CSV file with metadata', required=True)

    args = parser.parse_args()
    text = args.text
    metadata = args.metadata

    main()

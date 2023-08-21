"""
:author: Siméon FEREZ
:version: 1.0.0
:copyright: Copyright © 2023 by Siméon FEREZ. All rights reserved. This work may not be reproduced, in whole or in part, without the written permission of the author.
:description: Filter the Twitter data to only keep tweets in specified languages.

CLI Arguments:
    - --input, --i: Directory containing the raw data, or CSV File
    - --languages, --l: Languages to keep (Default: en es fr it de)

Examples:
    >>> python filter_language.py --input data.csv
    >>> python filter_language.py --input data.csv --languages en fr
"""

# -------------------------------------------------- IMPORTS -------------------------------------------------- #

# External
import pandas as pd
import os
import argparse

# -------------------------------------------------- GLOBALS -------------------------------------------------- #

LANGUAGES = ['en', 'es', 'fr', 'it', 'de']


# ------------------------------------------------- FUNCTIONS ------------------------------------------------- #


def process_file(fp):
    """
    Process a CSV file and remove tweets that are not in the specified languages.

    :param fp: file path
    :type fp: str
    :return: None
    :rtype: None

    >>> process_file('data.csv')
    """
    df = pd.read_csv(fp)

    if 'lang' in df.columns:
        l = len(df)
        df = df[df['lang'].isin(languages)]
        df.to_csv(fp, index=False)
        print(f'Cleaned {os.path.basename(fp)}, {l - len(df)} tweets removed')
    else:
        print(f'No language column (lang) in {os.path.basename(fp)}')


# -------------------------------------------------- MAIN -------------------------------------------------- #


def main():
    """
    Main function of the filter_language.py script.

    :return: None
    :rtype: None

    >>> main()
    """
    print(f'Filtering data with languages: {languages}')

    if os.path.isfile(input_):
        process_file(input_)
    else:
        for root, dirs, files in os.walk(input_):
            for file in files:
                if file.endswith(".csv"):
                    fp = os.path.join(root, file)
                    process_file(fp)


# -------------------------------------------------- CLI -------------------------------------------------- #

if __name__ == '__main__':
    """
    Command Line Interface of the filter_language.py script.
    
    Args:
        --input, --i: Directory containing the raw data, or CSV File
        --languages, --l: Languages to keep (Default: en es fr it de)
        
    Examples:
        >>> python filter_language.py --input data.csv
        >>> python filter_language.py --input data.csv --languages en fr
    """
    parser = argparse.ArgumentParser(description='Filter the raw data to only keep tweets in specified languages.')
    parser.add_argument('--input', '--i', type=str, help='Directory containing the raw data, or CSV File',
                        required=True)
    parser.add_argument('--languages', '--l', type=str, nargs='+', help='Languages to keep', default=LANGUAGES,
                        required=False)

    args = parser.parse_args()

    input_ = args.input
    languages = args.languages

    main()

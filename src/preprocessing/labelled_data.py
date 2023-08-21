"""
:author: Siméon FEREZ
:version: 1.0.0
:copyright: Copyright © 2023 by Siméon FEREZ. All rights reserved. This work may not be reproduced, in whole or in part, without the written permission of the author.
:description: Label a Twitter CSV file by adding a class column.

CLI Arguments:
    - --input, --i: CSV file or directory
    - --class_, --c: Class to labelled the data

Examples:
    >>> python labelled_data.py --input data.csv --class_ 1
"""

# -------------------------------------------------- IMPORTS -------------------------------------------------- #

# External
import pandas as pd
import argparse
import os
from tqdm import tqdm


# ------------------------------------------------- FUNCTIONS ------------------------------------------------- #

def process_file(fp):
    """
    Label a CSV file by adding a class column.

    :param fp: CSV file
    :type fp: str
    :return: None
    :rtype: None

    >>> process_file('data.csv')
    """
    df = pd.read_csv(fp)
    df['class'] = class_
    df.to_csv(fp, index=False)
    print(f'Labelled {fp}')


# ------------------------------------------------- MAIN ------------------------------------------------- #

def main():
    """
    Main function of the labelled_data.py script.

    :return: None
    :rtype: None

    >>> main()
    """
    print('Labelling data...')

    if os.path.isfile(input_):
        process_file(input_)
    else:

        for root, dirs, files in os.walk(input_):
            for file in tqdm(files):
                if file.endswith(".csv"):
                    fp = os.path.join(root, file)
                    process_file(fp)


# -------------------------------------------------- CLI -------------------------------------------------- #

if __name__ == '__main__':
    """
    Command Line Interface of the labelled_data.py script.
    
    Args:
        --input, --i: CSV file or directory
        --class_, --c: Class to labelled the data
        
    Examples:
        >>> python labelled_data.py --input data.csv --class_ 1
    """
    parser = argparse.ArgumentParser(description='Perform data cleaning on the raw linguistic data.')
    parser.add_argument('--input', '--i', type=str, help='Directory or CSV file', required=True)
    parser.add_argument('--class_', '--c', type=str, help='Class to labelled the data', required=True)

    args = parser.parse_args()

    input_ = args.input
    class_ = args.class_

    main()

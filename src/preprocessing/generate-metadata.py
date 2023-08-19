"""
:author: Siméon FEREZ
:version: 1.0.0
:copyright: Copyright © 2023 by Siméon FEREZ. All rights reserved. This work may not be reproduced, in whole or in part, without the written permission of the author.

Generate metadata for a Twitter CSV file, metadata will be the raw dataset without the text column.
"""

# -------------------------------------------------- IMPORTS -------------------------------------------------- #

# External
import pandas as pd
import argparse


# ------------------------------------------------- MAIN ------------------------------------------------- #

def main():
    """
    Main function of the generate-metadata.py script.
    :return: None
    :rtype: None
    >>> main()
    """
    print('Generating metadata...')

    df = pd.read_csv(input_)
    df = df.drop(columns=['text'])
    df.to_csv(f'{input_[:-4]}_metadata.csv', index=False)
    print(f'Metadata generated for {input_}')


# -------------------------------------------------- CLI -------------------------------------------------- #

if __name__ == '__main__':
    """
    Command Line Interface of the generate-metadata.py script.
    
    Args:
        --input, --i: CSV File
        
    Examples:
        >>> python generate-metadata.py --input data.csv
    """
    parser = argparse.ArgumentParser(description='Generate metadata for a CSV file.')
    parser.add_argument('--input', '--i', type=str, help='CSV file', required=True)

    args = parser.parse_args()

    input_ = args.input

    main()

"""
:author: Siméon FEREZ
:version: 1.0.0
:copyright: Copyright © 2023 by Siméon FEREZ. All rights reserved. This work may not be reproduced, in whole or in part, without the written permission of the author.
:description: Combine Twitter CSV files into one.

CLI Arguments:
    - --input, --i: Directory
    - --output, --o: Final file name (Default: combined.csv)

Examples:
    >>> python combine.py --input data/ --output combined.csv
"""

# ---------------------------------------------------- IMPORTS ------------------------------------------------------- #

# External
import argparse
import os
import pandas as pd
from tqdm import tqdm


# ---------------------------------------------------- SCRIPT -------------------------------------------------------- #

def main():
    """
    Main function, combines CSV files into one.

    :return: None
    :rtype: None

    >>> main()
    """
    full_paths = []
    for root, dirs, files in os.walk(input_):
        for file in files:
            if file.endswith(".csv"):
                full_paths.append(os.path.join(root, file))

    df = pd.read_csv(full_paths[0])
    for fp in tqdm(full_paths[1:]):
        df = pd.concat([df, pd.read_csv(fp)], ignore_index=True)

    l = len(df)
    df = df.drop_duplicates(subset=['tweet_id'])
    print(f'Dropped {l - len(df)} duplicates')
    df.to_csv(os.path.join(input_, output), index=False)

    print('COMBINED CSV FILES:')
    for fp in full_paths:
        print(fp.split('/')[-1])


# ---------------------------------------------------- MAIN ---------------------------------------------------------- #

if __name__ == "__main__":
    """
    Command Line Interface of the combine Twitter CSV files script.
    
    Args:
        --input, --i: Directory
        --output, --o: Final file name (Default: combined.csv)
        
    Examples:
        >>> python combine.py --input data/ --output combined.csv
    """
    parser = argparse.ArgumentParser(description='Combine CSV files')

    parser.add_argument('--input', '--i', type=str, help='Directory', required=True)
    parser.add_argument('--output', '--o', type=str, help='Final file name (Default: combined.csv)',
                        default='combined.csv')

    args = parser.parse_args()

    input_ = args.input
    output = args.output

    main()

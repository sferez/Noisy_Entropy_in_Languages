"""
:author: Siméon FEREZ
:version: 1.0.0
:copyright: Copyright © 2023 by Siméon FEREZ. All rights reserved. This work may not be reproduced, in whole or in part, without the written permission of the author.

Generate sub-datasets for a Twitter CSV file.
Sub-datasets will be grouped by a column and will contain tweet_id and text columns.
"""

# -------------------------------------------------- IMPORTS -------------------------------------------------- #

# External
import pandas as pd
import argparse
import os
from tqdm import tqdm


# ----------------------------------------------- FUNCTIONS ----------------------------------------------- #


def process_file(file):
    """
    Process a CSV file and generate sub-datasets grouped by a column.
    :param file: CSV file
    :type file: str
    :return: None
    :rtype: None
    >>> process_file('data.csv')
    """
    print(f'Processing {file}...')
    # df = pd.read_csv(input_)
    df = pd.read_csv(file, usecols=['tweet_id', 'text', group_by])
    if group_by == 'timestamp':
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        if unit == 'D':
            df['timestamp'] = df['timestamp'].dt.date
        elif unit == 'M':
            df['timestamp'] = df['timestamp'].dt.to_period('M')
        elif unit == 'Y':
            df['timestamp'] = df['timestamp'].dt.to_period('Y')
    df = df.groupby(group_by)

    if not os.path.exists(f'{file[:-4]}_by_{group_by}'):
        os.makedirs(f'{file[:-4]}_by_{group_by}')

    for group in df.groups:
        if len(df.get_group(group)) < min_size:
            continue
        df.get_group(group).drop(columns=[group_by]).to_csv(f'{file[:-4]}_by_{group_by}/{group}.csv', index=False)
        print(f'Sub-dataset generated for {group_by} = {group}')

    # Special for COVID DATASET
    # for group in df.groups:
    #     if not os.path.exists(f'{input_}_by_{group}'):
    #         os.makedirs(f'{input_}_by_{group}')
    #
    # for group in df.groups:
    #     if len(df.get_group(group)) < min_size:
    #         continue
    #     df.get_group(group).drop(columns=[group_by]).to_csv(f'{input_}_by_{group}/{os.path.basename(file)}', index=False)
    #     print(f'Sub-dataset generated for {group_by} = {group}')


# ------------------------------------------------- MAIN ------------------------------------------------- #

def main():
    """
    Main function of the generate-sub-df.py script.
    :return: None
    :rtype: None
    >>> main()
    """
    print(f'Generating sub-datasets for {input_} grouped by {group_by}...')

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
    Command Line Interface of the generate-sub-df.py script.
    
    Args:
        --input, --i: CSV file
        --group-by, --gb: Column to group by
        --unit, --u: If group-by is "timestamp" choose between "D" (day), "M" (month), "Y" (year)
        --min-size, --ms: Minimum size of a sub-dataset (default: 100)
        
    Examples:
        >>> python generate-sub-df.py --input data.csv --group-by lang
        >>> python generate-sub-df.py --input data.csv --group-by timestamp --unit D
        >>> python generate-sub-df.py --input data.csv --group-by timestamp --unit D --min-size 1000
    """
    parser = argparse.ArgumentParser(description='Generate sub-datasets for a CSV file.')
    parser.add_argument('--input', '--i', type=str, help='CSV file', required=True)
    parser.add_argument('--group-by', '--gb', type=str, help='Column to group by', required=True)
    parser.add_argument('--unit', '--u', type=str,
                        help='If group-by is "timestamp" choose between "D" (day), "M" (month), "Y" (year)',
                        required=False)
    parser.add_argument('--min-size', '--ms', type=int, help='Minimum size of a sub-dataset', default=100,
                        required=False)

    args = parser.parse_args()

    input_ = args.input
    group_by = args.group_by
    min_size = args.min_size
    if group_by == 'timestamp':
        unit = args.unit
        if unit not in ['D', 'M', 'Y']:
            raise ValueError('Add --unit argument. Unit must be one of "D" (day), "M" (month), "Y" (year)')

    main()

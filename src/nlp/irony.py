"""
:author: Siméon FEREZ
:version: 1.0.0
:copyright: Copyright © 2023 by Siméon FEREZ. All rights reserved. This work may not be reproduced, in whole or in part, without the written permission of the author.
:credits: TweetNLP: Cutting-Edge Natural Language Processing for Social Media. Camacho-Collados, J., Rezaee, K., Riahi, T., Ushio, A., Loureiro, D., Antypas, D., Boisson, J., Espinosa-Anke, L., Liu, F., Martinez-Cámara, E., & others (2022).
:description: Apply NLP Irony detection to a Twitter CSV file.

Hate Speech:
    - irony (1)
    - non-irony (0)

CLI Arguments:
    - --input, --i: Directory or CSV File
    - --force, --fo: Force detection (default: False)

Examples:
    >>> python3 irony.py --input data.csv
    >>> python3 irony.py --input data.csv --force
"""

# ----------------------------------------------- IMPORTS ----------------------------------------------- #

# External
import argparse
import pandas as pd
import os
from tqdm import tqdm
import tweetnlp
import subprocess

# ---------------------------------------------- CONSTANTS ---------------------------------------------- #

CHUNKSIZE = 10_000
BATCH_SIZE = 64


# ---------------------------------------------- FUNCTIONS ---------------------------------------------- #


def detect_irony(texts, batch_size=BATCH_SIZE):
    """
    Detects the irony of a list of texts using the TweetNLP model and returns the corresponding label-to-id.

    :param texts: texts to detect
    :type texts: list
    :param batch_size: batch size
    :type batch_size: int
    :return: list of label-to-id
    :rtype: list

    >>> detect_irony(['I am so happy', 'You are so funny'])
    >>> [0, 1]
    """
    irony = []
    for i in tqdm(range(0, len(texts), batch_size)):
        batch_texts = texts[i:i + batch_size]
        batch_irony = model.predict(batch_texts, batch_size=batch_size, skip_preprocess=True)
        irony.extend([1 if batch_ironic['label'] == 'irony' else 0 for batch_ironic in batch_irony])
    return irony


def process_file(fp):
    """
    Detects the irony of a CSV file using the TweetNLP model and saves the results in the same file.

    :param fp: file path
    :type fp: str
    :return: None
    :rtype: None

    >>> process_file('data.csv')
    """
    df = pd.read_csv(fp)

    if 'irony' in df.columns and not force:
        if df['irony'].isnull().sum() == 0:
            print('Already detected')
            return

    df['text'] = df['text'].astype(str)  # Avoids errors in the detection
    df['irony'] = detect_irony(df['text'].tolist())

    df.to_csv(fp, index=False)


def process_file_chunk(fp, num_lines):
    """
    Detects the irony of a CSV file using the TweetNLP model by chunks and saves the results in the same file.

    :param fp: file path
    :type fp: str
    :param num_lines: number of lines in the file
    :type num_lines: int
    :return: None
    :rtype: None

    >>> process_file_chunk('data.csv', 100_000)
    """
    print('Processing in chunks...')
    for i, df in tqdm(enumerate(pd.read_csv(fp, chunksize=CHUNKSIZE)), total=num_lines // CHUNKSIZE + 1):
        if 'irony' in df.columns and not force:
            if df['irony'].isnull().sum() == 0:
                print('Already detected')
                continue

        df['text'] = df['text'].astype(str)
        df['irony'] = detect_irony(df['text'].tolist())
        mode = 'a' if i != 0 else 'w'
        df.to_csv(f'{fp}.tmp', index=False, mode=mode, header=(i == 0))

    os.remove(fp)
    os.rename(f'{fp}.tmp', fp)


# ------------------------------------------------- MAIN ------------------------------------------------- #


def main():
    """
    Main function of the irony detection script.

    :return: None
    :rtype: None

    >>> main()
    """
    print(f'Irony detection on {input_}...')

    if os.path.isfile(input_):  # Single file
        fp = input_
        num_lines = int(subprocess.check_output(f"wc -l {fp}", shell=True).split()[0]) - 1
        if num_lines > CHUNKSIZE:
            process_file_chunk(fp, num_lines)
        else:
            process_file(fp)
    else:
        for root, dirs, files in os.walk(input_):
            for file in files:
                if file.endswith(".csv"):
                    print(file)
                    fp = os.path.join(root, file)
                    num_lines = int(subprocess.check_output(f"wc -l {fp}", shell=True).split()[0]) - 1
                    if num_lines > CHUNKSIZE:
                        process_file_chunk(fp, num_lines)
                    else:
                        process_file(fp)


# -------------------------------------------------- CLI -------------------------------------------------- #


if __name__ == "__main__":
    """
        Command Line Interface of the emotion detection script.

        Args:
            --input, --i: Directory or CSV File
            --force, --fo: Force detection (default: False)

        Examples:
            >>> python3 irony.py --input data.csv
            >>> python3 irony.py --input data.csv --force
        """
    parser = argparse.ArgumentParser(description='Apply NLP Irony detection to a CSV file.')

    parser.add_argument('--input', '--i', type=str, help='Directory or CSV File', required=True)
    parser.add_argument('--force', '--fo', action=argparse.BooleanOptionalAction, help='Force detection', default=False)

    args = parser.parse_args()
    input_ = args.input
    force = args.force

    model = tweetnlp.Irony()

    main()

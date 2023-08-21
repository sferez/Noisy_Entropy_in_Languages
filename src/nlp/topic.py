"""
:author: Siméon FEREZ
:version: 1.0.0
:copyright: Copyright © 2023 by Siméon FEREZ. All rights reserved. This work may not be reproduced, in whole or in part, without the written permission of the author.
:credits: TweetNLP: Cutting-Edge Natural Language Processing for Social Media. Camacho-Collados, J., Rezaee, K., Riahi, T., Ushio, A., Loureiro, D., Antypas, D., Boisson, J., Espinosa-Anke, L., Liu, F., Martinez-Cámara, E., & others (2022).
:description: Apply NLP Topic detection to a Twitter CSV file.

Topics:
    - unknown (0)
    - arts_&_culture (2)
    - business_&_entrepreneurs (3)
    - celebrity_&_pop_culture (4)
    - diaries_&_daily_life (5)
    - family (6)
    - fashion_&_style (7)
    - film_tv_&_video (8)
    - fitness_&_health (9)
    - food_&_dining (10)
    - gaming (11)
    - learning_&_educational (12)
    - music (13)
    - news_&_social_concern (14)
    - other_hobbies (15)
    - relationships (16)
    - science_&_technology (17)
    - sports (18)
    - travel_&_adventure (19)
    - youth_&_student_life (20)

CLI Arguments:
    - --input, --i: Directory or CSV File
    - --force, --fo: Force detection (default: False)

Examples:
    >>> python3 src/nlp/topic.py --input data.csv
    >>> python3 src/nlp/topic.py --input data.csv --force
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

def detect_topic(texts, batch_size=BATCH_SIZE):
    """
    Detects the topic of a list of texts using the TweetNLP model and returns the corresponding label-to-id.

    :param texts: texts to detect
    :type texts: list
    :param batch_size: batch size
    :type batch_size: int
    :return: list of label-to-id
    :rtype: list

    >>> detect_topic(['This was a great movie', 'Real Madrid won the Champions League'])
    >>> [7, 17]
    """
    topics = []
    for i in tqdm(range(0, len(texts), batch_size)):
        batch_texts = texts[i:i + batch_size]
        batch_topics = model.predict(batch_texts, batch_size=batch_size, skip_preprocess=True)
        topics.extend([label_to_id[topic['label'][0]] if len(topic['label']) > 0 else 0 for topic in batch_topics])
    return topics


def process_file(fp):
    """
    Detects the topic of a CSV file using the TweetNLP model and saves the corresponding label-to-id.

    :param fp: file path
    :type fp: str
    :return: None
    :rtype: None

    >>> process_file('data.csv')
    """
    df = pd.read_csv(fp)

    if 'topic' in df.columns and not force:
        if df['topic'].isnull().sum() == 0:
            print('Already detected')
            return

    df['text'] = df['text'].astype(str)  # Avoids errors in the detection
    df['topic'] = detect_topic(df['text'].tolist())

    df.to_csv(fp, index=False)


def process_file_chunk(fp, num_lines):
    """
    Detects the topic of a CSV file using the TweetNLP model by chunks and saves the corresponding label-to-id.

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
        if 'topic' in df.columns and not force:
            if df['topic'].isnull().sum() == 0:
                print('Already detected')
                continue

        df['text'] = df['text'].astype(str)  # Avoids errors in the detection
        df['topic'] = detect_topic(df['text'].tolist())
        mode = 'a' if i != 0 else 'w'
        df.to_csv(f'{fp}.tmp', index=False, mode=mode, header=(i == 0))

    os.remove(fp)
    os.rename(f'{fp}.tmp', fp)


# ------------------------------------------------- MAIN ------------------------------------------------- #


def main():
    """
    Main function of the topic detection script.

    :return: None
    :rtype: None

    >>> main()
    """
    print(f'Topic detection on {input_}...')

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
    Command Line Interface of the topic detection script.
    
    Args:
        --input, --i: Directory or CSV File
        --force, --fo: Force detection (default: False)
        
    Examples:
        >>> python3 src/nlp/topic.py --input data.csv
        >>> python3 src/nlp/topic.py --input data.csv --force
    """
    parser = argparse.ArgumentParser(description='Apply NLP Topic detection to a CSV file.')

    parser.add_argument('--input', '--i', type=str, help='Directory or CSV File', required=True)
    parser.add_argument('--force', '--fo', action=argparse.BooleanOptionalAction, help='Force detection', default=False)

    args = parser.parse_args()
    input_ = args.input
    force = args.force

    model = tweetnlp.load_model('topic_classification')

    # /!\ Note: Id 0 is reserved for the 'und' label, All the other labels are shifted by 1 /!\
    label_to_id = {v: int(k) + 1 for k, v in model.id_to_label.items()}
    label_to_id['und'] = 0

    main()

"""
:author: Siméon FEREZ
:version: 1.0.0
:copyright: Copyright © 2023 by Siméon FEREZ. All rights reserved. This work may not be reproduced, in whole or in part, without the written permission of the author.
:credits: TweetNLP: Cutting-Edge Natural Language Processing for Social Media. Camacho-Collados, J., Rezaee, K., Riahi, T., Ushio, A., Loureiro, D., Antypas, D., Boisson, J., Espinosa-Anke, L., Liu, F., Martinez-Cámara, E., & others (2022).
:description: Apply NLP Named Entity detection to a Twitter CSV file.

Entities:
    - person
    - location
    - event
    - corporation
    - product

CLI Arguments:
    - --input: Directory or CSV File
    - --lemmatize: Lemmatize entities (default: False)

Examples:
    >>> python namedEntity.py --input data.csv
    >>> python namedEntity.py --input data.csv --lemmatize
"""

# ----------------------------------------------- IMPORTS ----------------------------------------------- #

# External
import argparse
import pandas as pd
import os
from tqdm import tqdm
import tweetnlp
import spacy

# ----------------------------------------------- GLOBALS ----------------------------------------------- #

types = {'person', 'location', 'event', 'corporation', 'product'}
nlp = spacy.load("en_core_web_sm")
entities_list = []


# ---------------------------------------------- FUNCTIONS ---------------------------------------------- #

def lemmatize_entity(entity):
    """
    Lemmatizes an entity, i.e. returns the lemma of each word in the entity.

    :param entity: entity to lemmatize
    :type entity: str
    :return: lemmatized entity
    :rtype: str

    >>> lemmatize_entity('improvements')
    >>> 'improve'
    """
    return ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in nlp(entity)])


def detect_entity_w_lem(text):
    """
    Detects the entity of a text using the TweetNLP model and returns the corresponding label-to-id. Lemmatizes the entity.

    :param text: text to detect
    :type text: str
    :return: label-to-id
    :rtype: dict

    >>> detect_entity_w_lem('Elon Musk is the CEO of Tesla')
    >>> {'person': 'elon musk', 'corporation': 'tesla'}
    """
    result = model.predict(text)

    res = {}
    for r in result:
        if r['type'] in types:
            res[r['type']] = lemmatize_entity(r['entity'])

    return res


def detect_entity(text):
    """
    Detects the entity of a text using the TweetNLP model and returns the corresponding label-to-id.

    :param text: text to detect
    :type text: str
    :return: label-to-id
    :rtype: dict

    >>> detect_entity('Elon Musk is the CEO of Tesla')
    >>> {'person': 'Elon Musk', 'corporation': 'Tesla'}
    """
    result = model.predict(text)

    res = {}
    for r in result:
        if r['type'] in types:
            res[r['type']] = r['entity']

    return res


def process_file(fp):
    """
    Detects the entity of a CSV file using the TweetNLP model and saves the corresponding label-to-id.

    :param fp: file path
    :type fp: str
    :return: None
    :rtype: None

    >>> process_file('data.csv')
    """
    df = pd.read_csv(fp)

    df['text'] = df['text'].astype(str)  # Avoids errors in the detection
    df = df.drop(columns=['person', 'location', 'event', 'corporation', 'product'],
                 errors='ignore')  # drop columns if they exist
    tqdm.pandas()
    if lemmatize:
        df = pd.concat([df, df['text'].progress_apply(detect_entity_w_lem).apply(pd.Series)], axis=1)
    else:
        df = pd.concat([df, df['text'].progress_apply(detect_entity).apply(pd.Series)], axis=1)

    df.to_csv(fp, index=False)


# ------------------------------------------------- MAIN ------------------------------------------------- #


def main():
    """
    Main function of the named entity detection script.

    :return: None
    :rtype: None

    >>> main()
    """
    print(f'Named Entity detection on {input_} with lemmatization: {lemmatize}...')

    if os.path.isfile(input_):  # Single file
        fp = input_
        process_file(fp)
    else:
        for root, dirs, files in os.walk(input_):
            for file in files:
                if file.endswith(".csv"):
                    print(file)
                    fp = os.path.join(root, file)
                    process_file(fp)


# -------------------------------------------------- CLI -------------------------------------------------- #


if __name__ == "__main__":
    """
    Command Line Interface (CLI) of the named entity detection script.
    
    Args:
        --input: Directory or CSV File
        --lemmatize: Lemmatize entities (default: False)
        
    Examples:
        >>> python namedEntity.py --input data.csv
        >>> python namedEntity.py --input data.csv --lemmatize    
    """
    parser = argparse.ArgumentParser(description='Apply NLP Named Entity detection to a CSV file.')

    parser.add_argument('--input', '--i', type=str, help='Directory or CSV File', required=True)
    parser.add_argument('--lemmatize', '--l', action=argparse.BooleanOptionalAction, help='Lemmatize entities', default=False)

    args = parser.parse_args()
    input_ = args.input
    lemmatize = args.lemmatize

    model = tweetnlp.NER()

    main()

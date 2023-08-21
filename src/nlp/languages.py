"""
:author: Siméon FEREZ
:version: 1.0.0
:copyright: Copyright © 2023 by Siméon FEREZ. All rights reserved. This work may not be reproduced, in whole or in part, without the written permission of the author.
:credits: TweetNLP: Cutting-Edge Natural Language Processing for Social Media. Camacho-Collados, J., Rezaee, K., Riahi, T., Ushio, A., Loureiro, D., Antypas, D., Boisson, J., Espinosa-Anke, L., Liu, F., Martinez-Cámara, E., & others (2022).
:description: Apply NLP language detection to a Twitter CSV file.

Languages:
    - English (en)
    - French (fr)
    - German (de)
    - Italian (it)
    - Spanish (es)
    - ...

CLI Arguments:
    - --input, --i: Directory or CSV File
    - --fast, --fa: Use fast language detection (default: False)
    - --force, --fo: Force detection (default: False)

Examples:
    >>> python languages.py --input data.csv
    >>> python languages.py --input data.csv --fast
    >>> python languages.py --input data.csv --force
"""

# ----------------------------------------------- IMPORTS ----------------------------------------------- #

# External
import argparse
import pandas as pd
import os
from lingua import Language, LanguageDetectorBuilder
from tqdm import tqdm

# ---------------------------------------------- CONSTANTS ---------------------------------------------- #

# List of languages to use for detection
LANGUAGES = [Language.ENGLISH, Language.FRENCH, Language.GERMAN, Language.ITALIAN, Language.SPANISH]


# ---------------------------------------------- FUNCTIONS ---------------------------------------------- #


def detect_language(text):
    """
    Detects the language of a text using the Lingua model and returns the corresponding ISO 639-1 code.

    :param text: text to detect
    :type text: str
    :return: ISO 639-1 code
    :rtype: str

    >>> detect_language('I am so happy, I love you')
    >>> 'en'
    """
    result = detector.detect_language_of(text)
    if result:
        conf = detector.compute_language_confidence(text, result)
        if conf > 0.85:
            return result.iso_code_639_1.name.lower()
    return 'und'


def process_file(fp):
    """
    Detects the language of a CSV file and adds a 'lang' column.

    :param fp: file path
    :type fp: str
    :return: None
    :rtype: None

    >>> process_file('data.csv')
    """
    df = pd.read_csv(fp)

    if 'lang' in df.columns:
        if df['lang'].isnull().sum() == 0:
            print('Already detected')
            return

    df['text'] = df['text'].astype(str)  # Avoids errors in the detection
    tqdm.pandas()
    df['lang'] = df['text'].progress_apply(detect_language)

    df.to_csv(fp, index=False)


# ------------------------------------------------- MAIN ------------------------------------------------- #


def main():
    """
    Main function of the language detection script.

    :return: None
    :rtype: None

    >>> main()
    """
    print(f'Language detection on {input_}...')

    if os.path.isfile(input_):  # Single file
        fp = input_
        process_file(fp)
    else:
        for root, dirs, files in os.walk(input_):  # Directory
            for file in files:
                if file.endswith(".csv"):
                    print(file)
                    fp = os.path.join(root, file)
                    process_file(fp)


# -------------------------------------------------- CLI -------------------------------------------------- #


if __name__ == "__main__":
    """
    Command Line Interface of the language detection script.
    
    Args:
        --input, --i: Directory or CSV File
        --fast, --fa: Use fast language detection (default: False)
        --force, --fo: Force detection (default: False)
        
    Examples:
        >>> python languages.py --input data.csv
        >>> python languages.py --input data.csv --fast
        >>> python languages.py --input data.csv --force
    """
    parser = argparse.ArgumentParser(description='Apply NLP language detection to a CSV file.')

    parser.add_argument('--input', '--i', type=str, help='Directory or CSV File', required=True)
    parser.add_argument('--fast', '--fa', action=argparse.BooleanOptionalAction, help='Use fast language detection',
                        default=False)
    parser.add_argument('--force', '--fo', action=argparse.BooleanOptionalAction, help='Force detection', default=False)

    args = parser.parse_args()

    input_ = args.input
    fast = args.fast
    force = args.force

    if fast:
        print('Using fast language detection')
        detector = LanguageDetectorBuilder.from_languages(*LANGUAGES).with_low_accuracy_mode().build()
    else:
        detector = LanguageDetectorBuilder.from_languages(*LANGUAGES).build()

    # If you want to use all languages, uncomment the following line and comment the previous one
    # detector = LanguageDetectorBuilder.from_all_languages().with_preloaded_language_models().build()

    main()

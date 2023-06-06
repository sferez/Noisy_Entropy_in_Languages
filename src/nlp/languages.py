"""
Language NLP detection
"""

# ----------------------------------------------- IMPORTS ----------------------------------------------- #

# External
import argparse
import pandas as pd
import os
from lingua import Language, LanguageDetectorBuilder
from tqdm import tqdm

# ---------------------------------------------- CONSTANTS ---------------------------------------------- #

# List of languages to use for detection (can be changed)
LANGUAGES = [Language.ENGLISH, Language.FRENCH, Language.GERMAN, Language.ITALIAN, Language.SPANISH]


# ---------------------------------------------- FUNCTIONS ---------------------------------------------- #


def detect_language(text):
    result = detector.detect_language_of(text)
    if result:

        conf = detector.compute_language_confidence(text, result)
        if conf > 0.85:
            return result.iso_code_639_1.name.lower()
    return 'und'


# ------------------------------------------------- MAIN ------------------------------------------------- #


def main():

    print(f'Language detection on {input_dir}...')

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".csv"):
                print(file)
                fp = os.path.join(root, file)
                df = pd.read_csv(fp)

                if 'lang' in df.columns:
                    if df['lang'].isnull().sum() == 0:
                        print('Already detected')
                        continue

                df['text'] = df['text'].astype(str)  # Avoids errors in the detection
                tqdm.pandas()
                df['lang'] = df['text'].progress_apply(detect_language)

                df.to_csv(fp, index=False)


# -------------------------------------------------- CLI -------------------------------------------------- #


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Apply NLP language detection to a CSV file.')

    parser.add_argument('--input_dir', '--i', type=str, help='Directory', required=True)
    parser.add_argument('--fast', '--f', action=argparse.BooleanOptionalAction, help='Use fast language detection',
                        default=False)

    args = parser.parse_args()

    input_dir = args.input_dir
    fast = args.fast

    if fast:
        detector = LanguageDetectorBuilder.from_languages(*LANGUAGES).with_low_accuracy_mode().build()
    else:
        detector = LanguageDetectorBuilder.from_languages(*LANGUAGES).build()

    # If you want to use all languages, uncomment the following line and comment the previous one
    # detector = LanguageDetectorBuilder.from_all_languages().with_preloaded_language_models().build()

    main()

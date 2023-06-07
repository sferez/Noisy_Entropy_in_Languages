"""
Named Entity NLP detection
"""

# ----------------------------------------------- IMPORTS ----------------------------------------------- #

# External
import argparse
import pandas as pd
import os
from tqdm import tqdm
import tweetnlp

# ----------------------------------------------- GLOBALS ----------------------------------------------- #

types = {'person', 'location', 'event', 'corporation', 'product'}


# ---------------------------------------------- FUNCTIONS ---------------------------------------------- #


def detect_entity(text):
    result = model.predict(text)

    res = {}
    for r in result:
        if r['type'] in types:
            res[r['type']] = r['entity']

    return res

def process_file(fp):
    df = pd.read_csv(fp)


    df['text'] = df['text'].astype(str)  # Avoids errors in the detection
    tqdm.pandas()
    df = pd.concat([df, df['text'].progress_apply(detect_entity).apply(pd.Series)], axis=1)

    df.to_csv(fp, index=False)


# ------------------------------------------------- MAIN ------------------------------------------------- #


def main():
    print(f'Named Entity detection on {input_}...')

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
    parser = argparse.ArgumentParser(description='Apply NLP Named Entity detection to a CSV file.')

    parser.add_argument('--input', '--i', type=str, help='Directory or CSV File', required=True)
    # parser.add_argument('--force', '--fo', action=argparse.BooleanOptionalAction, help='Force detection', default=False)

    args = parser.parse_args()
    input_ = args.input
    # force = args.force

    model = tweetnlp.NER()

    main()

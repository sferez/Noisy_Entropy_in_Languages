"""
Topic NLP detection
"""

# ----------------------------------------------- IMPORTS ----------------------------------------------- #

# External
import argparse
import pandas as pd
import os
from tqdm import tqdm
import tweetnlp


# ---------------------------------------------- FUNCTIONS ---------------------------------------------- #


def detect_topic(text):
    topic = model.predict(text)

    if len(topic['label']) == 0:
        topic['label'] = ['und']

    return label_to_id[topic['label'][0]]


def process_file(fp):
    df = pd.read_csv(fp)

    if 'topic' in df.columns and not force:
        if df['topic'].isnull().sum() == 0:
            print('Already detected')
            return

    df['text'] = df['text'].astype(str)  # Avoids errors in the detection
    tqdm.pandas()
    df['topic'] = df['text'].progress_apply(detect_topic)

    df.to_csv(fp, index=False)


# ------------------------------------------------- MAIN ------------------------------------------------- #


def main():
    print(f'Topic detection on {input_}...')

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
    parser = argparse.ArgumentParser(description='Apply NLP Topic detection to a CSV file.')

    parser.add_argument('--input', '--i', type=str, help='Directory or CSV File', required=True)
    parser.add_argument('--force', '--fo', action=argparse.BooleanOptionalAction, help='Force detection', default=False)

    args = parser.parse_args()
    input_ = args.input
    force = args.force

    model = tweetnlp.load_model('topic_classification')

    # /!\ Note: Id 0 is reserved for the 'und' label, All the other labels are shifted by 1 /!\
    label_to_id = {v: int(k)+1 for k, v in model.id_to_label.items()}
    label_to_id['und'] = 0

    main()

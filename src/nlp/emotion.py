"""
Emotion NLP detection

Based on TweetNLP: Cutting-Edge Natural Language Processing for Social Media.
Camacho-Collados, J., Rezaee, K., Riahi, T., Ushio, A., Loureiro, D., Antypas, D., Boisson, J., Espinosa-Anke, L.,
Liu, F., Martinez-Cámara, E., & others (2022).
In Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing: System Demonstrations.
Association for Computational Linguistics.
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


def detect_emotion(texts, batch_size=BATCH_SIZE):
    emotions = []
    for i in tqdm(range(0, len(texts), batch_size)):
        batch_texts = texts[i:i + batch_size]
        topics = model.predict(batch_texts, batch_size=batch_size, skip_preprocess=True)
        emotions.extend([label_to_id[topic['label']] for topic in topics])
    return emotions


def process_file(fp):
    df = pd.read_csv(fp)

    if 'emotion' in df.columns and not force:
        if df['emotion'].isnull().sum() == 0:
            print('Already detected')
            return

    df['text'] = df['text'].astype(str)  # Avoids errors in the detection
    df['emotion'] = detect_emotion(df['text'].tolist())

    df.to_csv(fp, index=False)


def process_file_chunk(fp, num_lines):
    print('Processing in chunks...')
    for i, df in tqdm(enumerate(pd.read_csv(fp, chunksize=CHUNKSIZE)), total=num_lines // CHUNKSIZE + 1):
        if 'emotion' in df.columns and not force:
            if df['emotion'].isnull().sum() == 0:
                print('Already detected')
                continue

        df['text'] = df['text'].astype(str)  # Avoids errors in the detection
        df['emotion'] = detect_emotion(df['text'].tolist())
        mode = 'a' if i != 0 else 'w'
        df.to_csv(f'{fp}.tmp', index=False, mode=mode, header=(i == 0))

    os.remove(fp)
    os.rename(f'{fp}.tmp', fp)


# ------------------------------------------------- MAIN ------------------------------------------------- #


def main():
    print(f'Emotion detection on {input_}...')

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
    parser = argparse.ArgumentParser(description='Apply NLP Emotion detection to a CSV file.')

    parser.add_argument('--input', '--i', type=str, help='Directory or CSV File', required=True)
    parser.add_argument('--force', '--fo', action=argparse.BooleanOptionalAction, help='Force detection', default=False)

    args = parser.parse_args()
    input_ = args.input
    force = args.force

    model = tweetnlp.Emotion()

    label_to_id = {v: k for k, v in model.id_to_label.items()}
    #  'anger': '0',
    #  'anticipation': '1',
    #  'disgust': '2',
    #  'fear': '3',
    #  'joy': '4',
    #  'love': '5',
    #  'optimism': '6',
    #  'pessimism': '7',
    #  'sadness': '8',
    #  'surprise': '9',
    #  'trust': '10'

    main()

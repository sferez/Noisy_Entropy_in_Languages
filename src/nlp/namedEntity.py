"""
Named Entity NLP detection

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
import spacy

# ----------------------------------------------- GLOBALS ----------------------------------------------- #

types = {'person', 'location', 'event', 'corporation', 'product'}
nlp = spacy.load("en_core_web_sm")
entities_list = []


# ---------------------------------------------- FUNCTIONS ---------------------------------------------- #

def lemmatize_entity(entity):
    # Lemmatizes the entity
    return ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in nlp(entity)])


def detect_entity_w_lem(text):
    result = model.predict(text)

    res = {}
    for r in result:
        if r['type'] in types:
            res[r['type']] = lemmatize_entity(r['entity'])

    return res


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
    parser = argparse.ArgumentParser(description='Apply NLP Named Entity detection to a CSV file.')

    parser.add_argument('--input', '--i', type=str, help='Directory or CSV File', required=True)
    parser.add_argument('--lemmatize', '--l', action=argparse.BooleanOptionalAction, help='Lemmatize entities', default=False)

    args = parser.parse_args()
    input_ = args.input
    lemmatize = args.lemmatize

    model = tweetnlp.NER()

    main()

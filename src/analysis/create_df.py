"""
Create a dataframe from the results of the analysis.
"""

# ----------------------------------------------- IMPORTS ----------------------------------------------- #

import os
import pandas as pd
from datetime import datetime

# ---------------------------------------------- CONSTANTS ----------------------------------------------- #

sentiment_id = {
    0: "Neutral",
    1: "Positive",
    2: "Negative"
}

emotion_id = {
    0: 'anger',
    1: 'anticipation',
    2: 'disgust',
    3: 'fear',
    4: 'joy',
    5: 'love',
    6: 'optimism',
    7: 'pessimism',
    8: 'sadness',
    9: 'surprise',
    10: 'trust'
}

offensive_id = {
    0: "Not offensive",
    1: "Offensive"
}

hate_id = {
    0: "Not hate speech",
    1: "Hate speech"
}

irony_id = {
    0: "Not ironic",
    1: "Ironic"
}

topic_id = {
    0: "und",
    1: "arts_&_culture",
    2: "business_&_entrepreneurs",
    3: "celebrity_&_pop_culture",
    4: "diaries_&_daily_life",
    5: "family",
    6: "fashion_&_style",
    7: "film_tv_&_video",
    8: "fitness_&_health",
    9: "food_&_dining",
    10: "gaming",
    11: "learning_&_educational",
    12: "music",
    13: "news_&_social_concern",
    14: "other_hobbies",
    15: "relationships",
    16: "science_&_technology",
    17: "sports",
    18: "travel_&_adventure",
    19: "youth_&_student_life",
}


# ---------------------------------------------- FUNCTIONS ---------------------------------------------- #


def process_ppm(ppm_dir):
    ppm_entropy = pd.DataFrame()
    ppm_infor_content = pd.DataFrame()
    ppm_model_order = pd.DataFrame()
    ppm_distribution = pd.DataFrame()

    if os.path.exists(ppm_dir) and 'ppm' in ppm_dir:
        for file in os.listdir(ppm_dir):
            if file.endswith('txt') and not 'prediction' in file:
                file_path = os.path.join(ppm_dir, file)
                if "distribution" in file:
                    temp_data = pd.read_csv(file_path, sep='\t', header=None)
                    temp_data.columns = ['entropy']
                    if 'decay' in file:
                        temp_data['decay'] = True
                        temp_data['train'] = file.replace('_decay.txt', '').split('_')[-1]
                    else:
                        temp_data['decay'] = False
                        temp_data['train'] = file.replace('.txt', '').split('_')[-1]
                    ppm_distribution = pd.concat([ppm_distribution, temp_data])

                else:
                    temp_data = pd.read_csv(file_path, sep='\t', header=None)
                    temp_data['token_pos'] = range(1, len(temp_data) + 1)
                    if 'decay' in file:
                        temp_data['decay'] = True
                        temp_data['train'] = file.replace('_decay.txt', '').split('_')[-1]
                    else:
                        temp_data['decay'] = False
                        temp_data['train'] = file.replace('.txt', '').split('_')[-1]
                    type = 'entropy' if 'entropy' in file else 'information_content' if 'information' in file else 'model_order'
                    temp_data.columns = [type, 'token_pos', 'decay', 'train']

                    if type == 'entropy':
                        ppm_entropy = pd.concat([ppm_entropy, temp_data])
                    elif type == 'information_content':
                        ppm_infor_content = pd.concat([ppm_infor_content, temp_data])
                    else:
                        ppm_model_order = pd.concat([ppm_model_order, temp_data])

    return ppm_entropy, ppm_infor_content, ppm_model_order, ppm_distribution


def process_unigrams(unigram_dir):
    unigram_data = pd.DataFrame()

    if os.path.exists(unigram_dir) and 'unigrams' in unigram_dir:
        for file in os.listdir(unigram_dir):
            if file.endswith('.csv'):
                file_path = os.path.join(unigram_dir, file)
                temp_data = pd.read_csv(file_path)
                try:
                    temp_data['token_count'] = int(
                        file.split('_')[1].replace('.csv', ''))  # Get token count from file name
                except:
                    temp_data['token_count'] = int(300000)
                unigram_data = pd.concat([unigram_data, temp_data])

    return unigram_data


def process_hrate(hrate_dir):
    hrate_data = pd.DataFrame()
    if os.path.exists(hrate_dir) and 'hrate' in hrate_dir:
        for file in os.listdir(hrate_dir):
            if file.endswith('.csv'):
                file_path = os.path.join(hrate_dir, file)
                temp_data = pd.read_csv(file_path)
                hrate_data = pd.concat([hrate_data, temp_data])

    return hrate_data


def process_label(label, label_type):
    """
    Process a label to get the correct label name.
    :param label: The label to process.
    :param label_type: The type of label to process.
    :return: The processed label.
    """
    if label_type == 'emotion':
        return emotion_id[int(label)]
    elif label_type == 'offensive':
        return offensive_id[int(label)]
    elif label_type == 'hate':
        return hate_id[int(label)]
    elif label_type == 'irony':
        return irony_id[int(label)]
    elif label_type == 'topic':
        return topic_id[int(label)]
    elif label_type == 'sentiment':
        return sentiment_id[int(label)]
    elif label_type == 'date':
        return datetime.strptime(label, '%Y-%m-%d').date()
    elif label_type == 'file':
        return label


def process_single_analysis(directory):
    """
    Process the results of a single analysis.
    Return order:
        - ppm_entropy
        - ppm_infor_content
        - ppm_model_order
        - ppm_distribution
        - unigram_data
        - hrate_data
    :param directory: The directory containing the results of the analysis.
    :return: A tuple containing the processed dataframes.
    """
    ppm_entropy, ppm_infor_content, ppm_model_order, ppm_distribution = process_ppm(os.path.join(directory, 'ppm'))
    unigram_data = process_unigrams(os.path.join(directory, 'unigrams'))
    hrate_data = process_hrate(os.path.join(directory, 'hrate'))

    return ppm_entropy, ppm_infor_content, ppm_model_order, ppm_distribution, unigram_data, hrate_data


def process_multiple_analysis(main_dir, label_type):
    """
    Process the results of multiple analyses.
    label_type:
        - sentiment
        - topic
        - emotion
        - offensive
        - hate
        - date
        - irony
        - file
    Return order:
        - ppm_entropy
        - ppm_infor_content
        - ppm_model_order
        - ppm_distribution
        - unigram_data
        - hrate_data
    :param main_dir: The directory containing the results of the analyses.
    :param label_type: The type of label used for the analyses.
    :return: A tuple containing the processed dataframes.
    """
    if label_type not in ['sentiment', 'topic', 'emotion', 'offensive', 'hate', 'date', 'irony', 'file']:
        raise Exception(
            'Invalid label type, please choose from sentiment, topic, emotion, offensive, hate, date, irony, file')

    label_dirs = [os.path.join(main_dir, name) for name in os.listdir(main_dir) if
                  os.path.isdir(os.path.join(main_dir, name))]

    ppm_entropy = pd.DataFrame()
    ppm_infor_content = pd.DataFrame()
    ppm_model_order = pd.DataFrame()
    ppm_distribution = pd.DataFrame()
    unigram_data = pd.DataFrame()
    hrate_data = pd.DataFrame()

    for label_dir in label_dirs:
        ppm_entropy_temp, ppm_infor_content_temp, ppm_model_order_temp, ppm_distribution_temp, unigram_data_temp, hrate_data_temp = process_single_analysis(
            label_dir)

        label = label_dir.split('/')[-1]

        ppm_entropy_temp[label_type] = process_label(label, label_type)
        ppm_infor_content_temp[label_type] = process_label(label, label_type)
        ppm_model_order_temp[label_type] = process_label(label, label_type)
        ppm_distribution_temp[label_type] = process_label(label, label_type)
        unigram_data_temp[label_type] = process_label(label, label_type)
        hrate_data_temp[label_type] = process_label(label, label_type)

        ppm_entropy = pd.concat([ppm_entropy, ppm_entropy_temp])
        ppm_infor_content = pd.concat([ppm_infor_content, ppm_infor_content_temp])
        ppm_model_order = pd.concat([ppm_model_order, ppm_model_order_temp])
        ppm_distribution = pd.concat([ppm_distribution, ppm_distribution_temp])
        unigram_data = pd.concat([unigram_data, unigram_data_temp])
        hrate_data = pd.concat([hrate_data, hrate_data_temp])

    return ppm_entropy, ppm_infor_content, ppm_model_order, ppm_distribution, unigram_data, hrate_data

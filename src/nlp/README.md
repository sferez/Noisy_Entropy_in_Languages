# Natural Language Processing

Use Natural Language Processing (NLP) to analyze text data from tweets and attribute labels to them.

## Overview

The following NLP tasks are performed:
- [Emotion Detection](#Emotion-Detection)
- [Hate Speech Detection](#Hate-Speech-Detection)
- [Irony Detection](#Irony-Detection)
- [Language Detection](#Language-Detection)
- [Named Entity Detection](#Named-Entity-Detection)
- [Offensive Detection](#Offensive-Detection)
- [Sentiment Detection](#Sentiment-Detection)
- [Topic Detection](#Topic-Detection)


## Requirements

- Python

Main libraries:
- tweetnlp
- lingua


## Emotion Detection

The emotion detection script is designed to analyze tweets in a CSV file and determine the underlying emotion present in each tweet. Utilizing the TweetNLP model, this script can recognize a range of emotions and categorize them accordingly.

### Usage

To run the emotion detection script, use the following command:

```
python emotion.py --input data.csv
```

### Command Line Arguments

- `--input, --i`: Directory or CSV File (required)
- `--force, --fo`: Force detection, overriding existing results if present (default: False)

### Examples

You can run the emotion detection on a specific CSV file or directory with these commands:

```
python emotion.py --input data.csv
python emotion.py --input data.csv --force
```

### Output

The script will analyze the provided CSV file(s) and determine the emotion of each tweet. The results are added to a new 'emotion' column in the CSV file, using the following values:

- `anger (0)`
- `anticipation (1)`
- `disgust (2)`
- `fear (3)`
- `joy (4)`
- `love (5)`
- `optimism (6)`
- `pessimism (7)`
- `sadness (8)`
- `surprise (9)`
- `trust (10)`

### Processing Large Files

For handling large files, the script offers chunked processing. You can adjust the chunk size and batch size according to your system's capabilities.


## Hate Speech Detection

The hate speech detection script utilizes the TweetNLP model to analyze tweets in a CSV file and determine whether they contain hate speech or not. The results are appended to the original CSV file, indicating whether each tweet is classified as hate speech.

### Usage

To run the hate speech detection script, use the following command:

```
python hateSpeech.py --input data.csv
```

### Command Line Arguments

- `--input, --i`: Directory or CSV File (required)
- `--force, --fo`: Force detection, overriding existing results if present (default: False)

### Examples

You can run the hate speech detection on a specific CSV file or directory with these commands:

```
python hateSpeech.py --input data.csv
python hateSpeech.py --input data.csv --force
```

### Output

The script will analyze the provided CSV file(s) and determine whether each tweet contains hate speech. The results are added to a new 'hate' column in the CSV file, using the following values:

- `Non-hate: 0`
- `Hate: 1`

### Processing Large Files

For handling large files, the script offers chunked processing. You can adjust the chunk size and batch size according to your system's capabilities.


## Irony Detection

The irony detection script is designed to analyze the content of tweets in a CSV file and identify whether the text is ironic or not. The results are saved in the same CSV file with the detected irony label.

### Usage

To use the irony detection script, run the following command:

```
python3 irony.py --input data.csv
```

### Command Line Arguments

- `--input, --i`: Directory or CSV File (required)
- `--force, --fo`: Force detection even if the column already exists (default: False)

### Examples

You can apply irony detection to a specific CSV file or directory with the following commands:

```
python3 irony.py --input data.csv
python3 irony.py --input data.csv --force
```

### Output

The script will process the provided CSV file(s) and identify the irony in each tweet using the TweetNLP model. The detected irony will be added to the 'irony' column of the CSV file, represented as follows:

- `irony (1)`
- `non-irony (0)`

### Processing Large Files

For large files, the script offers chunked processing to handle the data more efficiently. The chunk size and batch size can be adjusted according to system capabilities.


## Language Detection

The language detection script is designed to analyze the content of tweets in a CSV file and identify the language of each tweet. It returns the corresponding ISO 639-1 code of the detected language and saves it in the same CSV file under the 'lang' column.

### Usage

To use the language detection script, run the following command:

```
python languages.py --input data.csv
```

### Command Line Arguments

- `--input, --i`: Directory or CSV File (required)
- `--fast, --fa`: Use fast language detection (default: False)
- `--force, --fo`: Force detection (default: False)

### Examples

You can apply language detection to a specific CSV file or directory with the following commands:

```
python languages.py --input data.csv
python languages.py --input data.csv --fast
python languages.py --input data.csv --force
```

### Output

The script will process the provided CSV file(s) and identify the language of each tweet using the Lingua model. The detected language will be added to the 'lang' column of the CSV file, represented by its ISO 639-1 code (e.g., 'en' for English).

### Fast Language Detection

By enabling the `--fast` option, the script will use a low accuracy mode for faster language detection. This mode may be useful for quickly processing large datasets but may have lower accuracy compared to the default mode.

### Supported Languages

The script is configured to detect the following languages:

- English (en)
- French (fr)
- German (de)
- Italian (it)
- Spanish (es)


## Named Entity Detection

The named entity detection script is designed to analyze the content of tweets in a CSV file and identify named entities such as persons, locations, events, corporations, and products. The identified entities are then saved in the same CSV file.

### Usage

To use the named entity detection script, run the following command:

```
python namedEntity.py
```

### Command Line Arguments

- `--input`: Directory or CSV File (required)
- `--lemmatize`: Lemmatize entities (default: False)

### Examples

You can apply named entity detection to a specific CSV file or directory with the following commands:

```
python namedEntity.py --input data.csv
python namedEntity.py --input data.csv --lemmatize
```

### Output

The script will process the provided CSV file(s) and identify the named entities using the TweetNLP model. The identified entities will be added to the CSV file as new columns corresponding to each type of entity: person, location, event, corporation, product.

### Lemmatization

If the `--lemmatize` option is enabled, the script will lemmatize the detected entities, meaning that it will convert each word in the entity to its base or root form (e.g., "improvements" will be converted to "improve").


## Offensive Detection

The offensive detection script is designed to analyze the content of tweets in a CSV file and classify them as offensive or not offensive. The following categories are identified:

- Offensive (1)
- Not Offensive (0)

### Usage

To use the offensive detection script, run the following command:

```
python3 offensive.py
```

### Command Line Arguments

- `--input, --i`: Directory or CSV File (required)
- `--force, --fo`: Force detection (default: False)

### Examples

You can apply offensive detection to a specific CSV file or directory with the following commands:

```
python3 offensive.py --input data.csv
python3 offensive.py --input data.csv --force
```

### Output

The script will process the provided CSV file(s) and classify the content as offensive or not offensive using the TweetNLP model. A "offensive" column will be added to the file, containing the numerical code for the corresponding classification.


## Sentiment Detection

The sentiment detection script applies NLP to identify the sentiment of content in a Twitter CSV file. The identified sentiments are:

- Positive (1)
- Negative (-1)
- Neutral (0)

### Usage

To use the sentiment detection script, run the following command:

```
python sentiment.py
```

### Command Line Arguments

- `--input, --i`: Directory or CSV File (required)
- `--force, --fo`: Force detection (default: False)

### Examples

You can apply sentiment detection to a specific CSV file or directory with the following commands:

```
python sentiment.py --input data.csv
python sentiment.py --input data.csv --force
```

### Output

The script will process the provided CSV file(s) and detect the sentiment using the TweetNLP model. A "sentiment" column will be added to the file, containing values of 1 for positive sentiment, -1 for negative sentiment, and 0 for neutral sentiment.


## Topic Detection

The topic detection script applies NLP to categorize the content of tweets in a CSV file into predefined topics. The identified topics include but are not limited to:

- Unknown (0)
- Arts & Culture (2)
- Business & Entrepreneurs (3)
- Celebrity & Pop Culture (4)
- Fitness & Health (9)
- Science & Technology (17)
- Travel & Adventure (19)

### Usage

To use the topic detection script, run the following command:

```
python3 src/nlp/topic.py
```

### Command Line Arguments

- `--input, --i`: Directory or CSV File (required)
- `--force, --fo`: Force detection (default: False)

### Examples

You can apply topic detection to a specific CSV file or directory with the following commands:

```
python3 src/nlp/topic.py --input data.csv
python3 src/nlp/topic.py --input data.csv --force
```

### Output

The script will process the provided CSV file(s) and detect the topic using the TweetNLP model. A "topic" column will be added to the file, containing the numerical code for the corresponding topic.



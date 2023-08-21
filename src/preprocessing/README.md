# Pre-processing

The pre-processing scripts are used to prepare the data for the NLP scripts and Entropy Estimation scripts.

The scripts are divided into the following categories:
- Cleaning
- Data Manipulation (e.g. splitting, merging, etc.)
- Tokenization

They should be run in the above order.

## Overview

Cleaning scripts:
- [Code Cleaning](#code-cleaning)
- [Twitter Data Cleaning](#twitter-data-cleaning)

Data Manipulation scripts:
- [Twitter CSV File Combination](#twitter-csv-file-combination)
- [Twitter CSV Metadata Combination](#twitter-csv-metadata-combination)
- [Vocabulary File Combination](#vocabulary-file-combination)
- [Metadata Generation for Twitter CSV File](#metadata-generation-for-twitter-csv-file)
- [Generate Sub-Datasets for Twitter CSV File](#generate-sub-datasets-for-twitter-csv-file)
- [Filter Twitter Data by Language](#filter-twitter-data-by-language)
- [Label Twitter Data with Class](#label-twitter-data-with-class)

Tokenization scripts:
- [Tokenize Programming Language CSV File](#tokenize-programming-language-csv-file)
- [Tokenize Raw Linguistic Data Text Files](#tokenize-raw-linguistic-data-text-files)
- [Tokenize a Twitter CSV File](#tokenize-a-twitter-csv-file)

## Requirements

- Python

Main libraries:
- Pandas
- NLTK

## Code Cleaning

The code cleaning script is a powerful tool that processes source code files to remove or keep specific elements like variables, functions, numbers, strings, and comments. The script can process files written in Java, Python, or C++.

### Usage

To run the code cleaning script, use the following command:

```
python clean_code.py --input data.tsv --lang Python
```

### Command Line Arguments

- `--input, --i`: Directory or TSV File (required)
- `--lang, --l`: Language: Java, Python, C++ (required)
- `--debug, --d`: Debug, get replacements details in the output file (default: False)
- `--var, --v`: Keep variables (default: False)
- `--number, --num`: Keep numbers (default: False)
- `--comments, --com`: Keep comments (default: False)
- `--string, --s`: Keep strings (default: False)

### Examples

Here are some examples of using the script:

- To clean Python code from a file, removing all variables, numbers, comments, and strings:
  ```
  python clean_code.py --input data.tsv --lang Python
  ```

- To clean Python code and keep variables and numbers, with debugging information:
  ```
  python clean_code.py --input data.tsv --lang Python --debug --var --num
  ```

### Output

The script will process the provided TSV file(s) or directory, removing or keeping the specified elements. The cleaned code will be written to a new CSV file, with the option to include debug information.

### Debugging

By enabling the debug mode, the script will generate additional text files containing details about the replacements made. This includes information about removed variables, functions, comments, numbers, and strings.

## Twitter Data Cleaning

This script is designed to clean Twitter CSV files, providing the option to remove or keep various elements like punctuation, accents, emojis, mentions, URLs, extra spaces, RT tags, and case transformation.

### Usage

To run the Twitter data cleaning script, use the following command:

```
python clean_tweets.py --input data.csv --output data-cleaned
```

### Command Line Arguments

- `--input, --i`: Directory containing the raw data, or CSV File (required)
- `--output, --o`: Directory to save the scraping-cleaned data (required)
- `--punctuation, --p`: Keep punctuation (default: False)
- `--accents, --a`: Keep accents (default: False)
- `--emojis, --e`: Keep emojis (default: False)
- `--mentions, --m`: Keep mentions (default: False)
- `--urls, --u`: Keep URLs (default: False)
- `--spaces, --s`: Keep extra spaces (default: False)
- `--rt, --r`: Keep RT Tags (default: False)
- `--lowercase, --l`: Keep all cases (default: False)

### Examples

Here are some examples of using the script:

- To clean the Twitter data from a file, removing all the specified elements:
  ```
  python clean_tweets.py --input data.csv --output data-cleaned
  ```

- To clean the Twitter data and keep punctuation:
  ```
  python clean_tweets.py --input data.csv --output data-cleaned --punctuation
  ```

- To clean the Twitter data and keep punctuation, accents, and emojis:
  ```
  python clean_tweets.py --input data.csv --output data-cleaned --punctuation --accents --emojis
  ```

### Output

The script will process the provided CSV file(s) or directory, removing or keeping the specified elements. The cleaned data will be written to a new CSV file.


## Twitter CSV File Combination

The script provided is tailored to combine multiple Twitter CSV files located within a specified directory into one single CSV file. This can be particularly useful when dealing with segmented data or merging results from various sources.

### Usage

To run the Twitter CSV file combination script, use the following command:

```
python combine.py --input data/ --output combined.csv
```

### Command Line Arguments

- `--input, --i`: Directory containing the CSV files that need to be combined (required)
- `--output, --o`: Final file name for the combined CSV (default: `combined.csv`)

### Examples

Here's an example of how to use the script:

- To combine all the CSV files in the `data/` directory and save the result as `combined.csv`:
  ```
  python combine.py --input data/ --output combined.csv
  ```

### Output

The script will process the provided directory and combine all CSV files found within, removing any duplicates based on the 'tweet_id' field. The combined data will be written to the specified output file.


## Twitter CSV Metadata Combination

This script is designed to combine metadata with a Twitter CSV file. This process involves merging two CSV files: one containing the text data (e.g., tweets) and the other containing corresponding metadata. The combined file is then saved, providing a richer dataset for analysis.

### Usage

To run the Twitter CSV metadata combination script, use the following command:

```
python combine_metadata.py --text data/combined.csv --metadata data/metadata.csv
```

### Command Line Arguments

- `--text, --t`: CSV file containing the text data (e.g., tweets) (required)
- `--metadata, --m`: CSV file containing the corresponding metadata (required)

### Examples

Here's an example of how to use the script:

- To combine the text data in `data/combined.csv` with metadata from `data/metadata.csv`:
  ```
  python combine_metadata.py --text data/combined.csv --metadata data/metadata.csv
  ```

### Output

The script will read the specified text and metadata CSV files, merge them, and then save the combined data to the location specified in the `--text` argument. Any rows with missing data will be dropped from the final CSV file.


## Vocabulary File Combination

The vocabulary file combination script is designed to merge multiple vocabulary files (`.txt`) into a single consolidated vocabulary file. This can be useful for aggregating vocabulary from different sources or datasets into one unified vocabulary list.

### Usage

To run the vocabulary file combination script, use the following command:

```
python combine_vocab.py --input data
```

### Command Line Arguments

- `--input, --i`: Directory containing the vocabulary files (required).
- `--output, --o`: Final file name for the combined vocabulary file (default: `vocab-combined.txt`).

### Examples

Here are some examples of how to use the script:

- To combine vocabulary files from the `data` directory:
  ```
  python combine_vocab.py --input data
  ```

- To combine vocabulary files from the `data` directory and save the result as `final_vocab.txt`:
  ```
  python combine_vocab.py --input data --output final_vocab.txt
  ```

### Output

The script will process all vocabulary files in the specified directory that have 'vocab' in their name and end with the `.txt` extension (excluding any that end with `combined.txt`). It will combine the unique vocabulary tokens from these files into the specified output file.

The final result is a single text file containing all unique vocabulary tokens from the input files, with each token on a new line.


## Metadata Generation for Twitter CSV File

The metadata generation script is specifically designed to create a metadata file from a given Twitter CSV file. The generated metadata will contain all the columns from the original CSV file except the text column. This can be useful for analyses that require metadata without the actual text content.

### Usage

To run the metadata generation script, use the following command:

```
python generate_metadata.py --input data.csv
```

### Command Line Arguments

- `--input, --i`: CSV File containing the original data (required).

### Examples

Here's an example of how to use the script:

- To generate metadata for a CSV file named `data.csv`:
  ```
  python generate_metadata.py --input data.csv
  ```

### Output

The script will process the provided CSV file, removing the `text` column, and write the remaining columns to a new CSV file with the suffix `_metadata.csv`.

For example, if the input file is `data.csv`, the metadata file will be named `data_metadata.csv`.



## Generate Sub-Datasets for Twitter CSV File

This script is designed to create sub-datasets from a given Twitter CSV file. The sub-datasets are grouped by a specified column, and each resulting sub-dataset will contain only the `tweet_id` and `text` columns.

### Usage

To run the script to generate sub-datasets, use the following command:

```
python generate_sub_df.py --input data.csv --group-by lang
```

### Command Line Arguments

- `--input, --i`: CSV file containing the original data (required).
- `--group-by, --gb`: Column to group by (required).
- `--unit, --u`: If the group-by column is "timestamp," choose between "D" (day), "M" (month), "Y" (year) (optional).
- `--min-size, --ms`: Minimum size of a sub-dataset (default: 100).

### Examples

Here are some examples of how to use the script:

- To generate sub-datasets grouped by language:
  ```
  python generate_sub_df.py --input data.csv --group-by lang
  ```

- To generate sub-datasets grouped by timestamp, with daily granularity:
  ```
  python generate_sub_df.py --input data.csv --group-by timestamp --unit D
  ```

- To generate sub-datasets grouped by timestamp, with daily granularity, and a minimum sub-dataset size of 1000:
  ```
  python generate_sub_df.py --input data.csv --group-by timestamp --unit D --min-size 1000
  ```

### Output

The script will process the provided CSV file and generate sub-datasets grouped by the specified column. The sub-datasets will be saved as individual CSV files in a directory named after the input file and grouping column, such as `data_by_lang`.

Each sub-dataset CSV file will be named according to the unique value of the grouping column.










## Filter Twitter Data by Language

This script is designed to filter Twitter data by language, allowing you to keep only the tweets in specified languages.

### Usage

To run the script to filter the Twitter data, use the following command:

```
python filter_language.py --input data.csv
```

### Command Line Arguments

- `--input, --i`: Directory containing the raw data or a specific CSV file (required).
- `--languages, --l`: List of languages to keep (default: en, es, fr, it, de).

### Examples

Here are some examples of how to use the script:

- To filter the data and keep only tweets in English, Spanish, French, Italian, and German:
  ```
  python filter_language.py --input data.csv
  ```

- To filter the data and keep only tweets in English and French:
  ```
  python filter_language.py --input data.csv --languages en fr
  ```

### Output

The script will process the provided CSV file or directory of files and remove tweets that are not in the specified languages. The filtered data will be saved in the same CSV file(s), and a summary of the number of tweets removed will be printed.

### Requirements

- The script expects the CSV file(s) to contain a column named `lang` that specifies the language of each tweet.












## Label Twitter Data with Class

This script is designed to label a Twitter CSV file by adding a class column, allowing you to classify the data with a specific label.

### Usage

To run the script and label the data with a specific class, use the following command:

```bash
python labelled_data.py --input data.csv --class_ 1
```

### Command Line Arguments

- `--input, --i`: The path to the CSV file or directory containing the data to be labeled (required).
- `--class_, --c`: The class to label the data with (required).

### Examples

Here's an example of how to use the script:

- To label the data in the file `data.csv` with class 1:
  ```bash
  python labelled_data.py --input data.csv --class_ 1
  ```

### Output

The script will process the specified CSV file or directory of files and add a new column named `class`, filled with the specified class label. The labeled data will be saved in the same CSV file(s), and a message confirming the labeling will be printed.



## Tokenize Programming Language CSV File

The provided script tokenizes a programming language CSV file. You can perform either word-level or character-level tokenization and generate n-grams from the tokens.

### Usage

To run the script, use the following command:

```bash
python tokenize_code.py --input data.csv
```

### Command Line Arguments

- `--input, --i`: The path to the CSV file or directory containing the data to be tokenized (required).
- `--char, --c`: To perform character-level tokenization (default is word-level).
- `--ngrams, --n`: To generate n-grams from the tokens (default: 1).

### Examples

Here are some examples of how to use the script:

- To tokenize the data in the file `data.csv`:
  ```bash
  python tokenize_code.py --input data.csv
  ```

- To perform character-level tokenization:
  ```bash
  python tokenize_code.py --input data.csv --char
  ```

- To generate 3-grams from the tokens:
  ```bash
  python tokenize_code.py --input data.csv --ngrams 3
  ```

- To perform character-level tokenization and generate 3-grams:
  ```bash
  python tokenize_code.py --input data.csv --char --ngrams 3
  ```

### Output

The script will process the specified CSV file(s) and generate three output files:

1. A token file containing the extracted tokens.
2. A vocab file containing the unique tokens.
3. A PPM (Prediction by Partial Matching) format token file.

The files will be named according to the tokenization method (character or word level) and the n-gram size.

## Tokenize Raw Linguistic Data Text Files

The provided script is designed to tokenize raw linguistic data from text files. You can tokenize the data at the word or character level, and you can also generate n-grams from the tokens.

### Usage

To run the script, use the following command:

```bash
python tokenize_text.py --input data.txt
```

### Command Line Arguments

- `--input, --i`: Path to the text file or directory containing the data to be tokenized (required).
- `--ngrams, --n`: Option to generate n-grams from the tokens (default: 1).
- `--chars, --c`: Option to tokenize at the character level instead of word level (default: False).

### Examples

Here are some examples of how to use the script:

- To tokenize the data in the file `data.txt`:
  ```bash
  python tokenize_text.py --input data.txt
  ```

- To generate 2-grams from the tokens:
  ```bash
  python tokenize_text.py --input data.txt --ngrams 2
  ```

- To tokenize at the character level and generate 2-grams:
  ```bash
  python tokenize_text.py --input data.txt --ngrams 2 --chars
  ```

### Output

The script will process the specified text file(s) and generate three output files:

1. A token file containing the extracted tokens.
2. A vocab file containing the unique tokens.
3. A PPM (Prediction by Partial Matching) format token file.

The files will be named according to the tokenization method (character or word level) and the n-gram size.

## Tokenize a Twitter CSV File

The provided script is designed to tokenize the text content of Twitter data stored in a CSV file. This can be performed at the word or character level, and n-grams can be generated from the tokens.

### Usage

To run the script, use the following command:

```bash
python tokenize_tweets.py --input data.csv
```

### Command Line Arguments

- `--input, --i`: Path to the CSV file or directory containing the data to be tokenized (required).
- `--ngrams, --n`: Option to generate n-grams from the tokens (default: 1).
- `--chars, --c`: Option to tokenize at the character level instead of word level (default: False).

### Examples

Here are some examples of how to use the script:

- To tokenize the data in the file `data.csv`:
  ```bash
  python tokenize_tweets.py --input data.csv
  ```

- To generate 2-grams from the tokens:
  ```bash
  python tokenize_tweets.py --input data.csv --ngrams 2
  ```

- To tokenize at the character level and generate 2-grams:
  ```bash
  python tokenize_tweets.py --input data.csv --ngrams 2 --chars
  ```

### Output

The script will process the specified CSV file(s) and generate three output files:

1. A token file containing the extracted tokens.
2. A vocab file containing the unique tokens.
3. A PPM (Prediction by Partial Matching) format token file.

The files will be named according to the tokenization method (character or word level) and the n-gram size.
# Entropy Estimation

The entropy estimation used different methods to estimate the entropy of the text. The methods used are:
- Plug-in Estimators (unigrams)
  - Maximum Likelihood (ML)
  - Miller-Maddow (MM)
  - Chao-Shen (CS)
  - Schurmann-Grassberger (SG)
  - Shrinkage (SH)
  - Laplace
  - Jeffrey
  - Minimax
  - NSB
- Entropy Rate
- Prediction by Partial Matching (PPM)

On top of the entropy estimators Bootstrap is used to estimate the confidence interval of the entropy.

**Note:** The scripts are run from Python and the entropy estimators are implemented in R.

## Overview

Single Entropy Estimation:
- [Plug-in Estimators](#plug-in-estimators)
- [Entropy Rate](#entropy-rate)
- [PPM Entropy](#ppm-entropy)

Full Analysis:
- [Full Analysis Script](#full-analysis-script)
- [Full Analysis Directory Script](#full-analysis-directory-script)


## Requirements

- Python
- R

## Plug-in Estimators

The provided script is designed to estimate the entropy of a given distribution of tokens using Plug-in entropy estimation. The script calculates entropy using two methods: a built-in R script and the NSB (Nemenman-Schafee-Bialek) method.

### Usage

To run the script, use the following command:

```bash
python3 src/entropyEstimation/entropy.py --tokens tokens.txt --vocab vocab.txt
```

### Command Line Arguments

- `--tokens, --t`: Path to the list of tokens (required).
- `--vocab, --v`: Path to the vocabulary file (optional). If not provided, all tokens will be considered as vocabulary.
- `--max_tokens, --mt`: Maximum number of tokens to consider (optional).
- `--bootstrap, --b`: Whether to perform bootstrap analysis (optional).
- `--output_dir, --o`: Path to the output directory (optional).

### Examples

Here are some examples of how to use the script:

- To estimate entropy with a specific vocabulary file:
  ```bash
  python3 src/entropyEstimation/entropy.py --tokens tokens.txt --vocab vocab.txt
  ```

- To estimate entropy with a maximum number of tokens and bootstrap analysis:
  ```bash
  python3 src/entropyEstimation/entropy.py --tokens tokens.txt --max_tokens 1000 --bootstrap
  ```

### Output

The script will produce a CSV file with the results of the entropy estimation. The output includes the entropy value, standard deviation, mean absolute error (MAE), mean squared error (MSE), and confidence interval (CI) if bootstrap analysis is performed.
The output also contains graphs of the entropy estimation and the bootstrap analysis.

## Entropy Rate

The provided script is designed to estimate the entropy rate of a given corpus using Entropy Rate estimation. The calculation is performed by calling an R script, and the results are saved to the specified output directory.

### Usage

To run the script, use the following command:

```bash
python3 src/entropyEstimation/Hrate.py --tokens tokens.txt
```

### Command Line Arguments

- `--tokens`: Path to the list of tokens (required).
- `--max_tokens`: Maximum number of tokens to consider (optional).
- `--fast`: Whether to use the fast version of the algorithm (optional).
- `--output_dir`: Path to the output directory (optional).

### Examples

Here are some examples of how to use the script:

- To estimate the entropy rate with a specific token file:
  ```bash
  python3 src/entropyEstimation/Hrate.py --tokens tokens.txt
  ```

- To estimate the entropy rate with a maximum number of tokens and the fast version of the algorithm:
  ```bash
  python3 src/entropyEstimation/Hrate.py --tokens tokens.txt --max_tokens 100000 --fast
  ```

### Output

The script will produce an output file with the results of the entropy rate estimation in the specified output directory.



## PPM Entropy

The provided script is designed to estimate the entropy of a given corpus using Prediction by Partial Matching (PPM) entropy estimation. The calculation is performed by calling an external R script, and the results are saved to the specified output directory.

### Usage

To run the script, use the following command:

```bash
python3 src/entropyEstimation/ppm.py --tokens tokens.txt --vocab vocab.txt
```

### Command Line Arguments

- `--tokens`: Path to the list of tokens (required).
- `--vocab`: Path to the list of vocabulary (required).
- `--max_train`: Maximum number of training samples to consider (optional).
- `--decay`: Whether to use the decay version of the algorithm (optional).
- `--output_dir`: Path to the output directory (optional).

### Examples

Here are some examples of how to use the script:

- To estimate the PPM entropy with a specific token file and vocabulary:
  ```bash
  python3 src/entropyEstimation/ppm.py --tokens tokens.txt --vocab vocab.txt
  ```

- To estimate the PPM entropy with decay and a maximum number of training samples:
  ```bash
  python3 src/entropyEstimation/ppm.py --tokens tokens.txt --vocab vocab.txt --decay --max_train 5000
  ```

### Output

The script will produce an output file with the results of the PPM entropy estimation in the specified output directory.






## Full Analysis Script

The provided script is designed to run a comprehensive analysis of entropy estimation for a given corpus, including unigram entropy estimation, PPM (Prediction by Partial Matching) entropy estimation, and Hrate (Entropy Rate) entropy estimation.

### Usage

To run the script, use the following command:

```bash
python3 src/entropyEstimation/full_analysis.py --tokens tokens.txt --vocab vocab.txt
```

### Command Line Arguments

- `--tokens, --t`: Path to the list of tokens (required).
- `--vocab, --v`: Path to the vocabulary file (optional).
- `--use_vocab, --uv`: Whether to use vocabulary for unigram entropy estimation (default: False).
- `--unigrams, --u`: Skip unigram entropy estimation (optional).
- `--ppm, --p`: Skip PPM entropy estimation (optional).
- `--hrate, --h`: Skip Hrate entropy estimation (optional).
- `--fast, --f`: Skip PPM entropy estimation, and uncertainty analysis (optional).
- `--output_dir, --o`: Path to the output directory (default: results/\<file_name>).

### Examples

Here are some examples of how to use the script:

- Run the full analysis for tokens and vocabulary files:
  ```bash
  python3 src/entropyEstimation/full_analysis.py --tokens tokens.txt --vocab vocab.txt
  ```

- Run the full analysis but skip unigram entropy estimation:
  ```bash
  python3 src/entropyEstimation/full_analysis.py --tokens tokens.txt --vocab vocab.txt --unigrams
  ```

- Run the fast version of the analysis (skipping PPM and uncertainty analysis):
  ```bash
  python3 src/entropyEstimation/full_analysis.py --tokens tokens.txt --vocab vocab.txt --fast
  ```

### Output

The script will produce output files with the results of the entropy estimations in the specified output directory.


## Full Analysis Directory Script

The provided script is designed to run the full analysis of entropy estimation on a directory of files. This includes unigram entropy estimation, PPM (Prediction by Partial Matching) entropy estimation, and Hrate (Entropy Rate) estimation. The script will analyze all files in the specified directory, which should contain corresponding token and vocabulary files.

### Usage

To run the script, use the following command:

```bash
python3 src/entropyEstimation/run_dir.py --input_dir data/
```

### Command Line Arguments

- `--input_dir, --i`: Path to the directory containing files to analyze (required).
- `--fast, --f`: Whether to use the fast version of the algorithm (optional).
- `--vocab, --v`: Path to the vocabulary file if using a global vocabulary for the whole directory (optional).

### Examples

Here are some examples of how to use the script:

- Run the full analysis on the directory and use the fast version:
  ```bash
  python3 src/entropyEstimation/run_dir.py --input_dir data/ --fast
  ```

- Run the full analysis on the directory using a global vocabulary file:
  ```bash
  python3 src/entropyEstimation/run_dir.py --input_dir data/ --vocab vocab.txt
  ```

### Output

The script will produce output files with the results of the entropy estimations in the specified output directory for each file in the directory.

"""
Run analysis on a directory of files.
"""

# --------------------------------------------- IMPORTS --------------------------------------------- #

# External
import os
import argparse


# ----------------------------------------------- MAIN ----------------------------------------------- #


def main():
    if os.path.isdir(os.path.join(dir)):
        all_files = os.listdir(os.path.join(dir))

        # process the csv files
        for file in all_files:
            if file.endswith('.csv'):
                filename = os.path.join(dir, file)

                # remove the .csv from the name
                file_no_ext = file[:-4]

                # find the corresponding token and vocab files
                for token_file in all_files:
                    if token_file.startswith(file_no_ext) and "tokens" in token_file and "ppm" not in token_file:
                        tokens = os.path.join(dir, token_file)
                for vocab_file in all_files:
                    if vocab_file.startswith(file_no_ext) and "vocab" in vocab_file:
                        vocab = os.path.join(dir, vocab_file)

                output_dir = os.path.join(dir.split("/")[-1], file_no_ext)

                if global_vocab:
                    vocab = global_vocab

                print(filename)
                print(tokens)
                print(vocab)
                print(output_dir)
                os.system(
                    f'python3 src/entropyEstimation/full-analysis.py --t {tokens} --v {vocab} --o {output_dir} {"--f" if fast else ""} {"--uv" if global_vocab else ""}')
                print("------------------------------------------------------------")


# ----------------------------------------------- CLI ----------------------------------------------- #

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run analysis on a directory of files.")
    parser.add_argument('--input_dir', '--i', type=str, help="Directory containing files to analyze.")
    parser.add_argument('--fast', '--f', action=argparse.BooleanOptionalAction, default=False, help='Fast mode')
    parser.add_argument('--vocab', '--v', type=str,
                        help='Path to vocabulary, if using a global one for the whole directory', default=None,
                        required=False)

    args = parser.parse_args()
    dir = args.input_dir
    fast = args.fast
    global_vocab = args.vocab

    main()

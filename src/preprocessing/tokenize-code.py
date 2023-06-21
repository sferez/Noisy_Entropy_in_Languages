'''
Tokenize computer language data.
'''
import gc
# -------------------------------------------------- IMPORTS -------------------------------------------------- #

# External
from ast import literal_eval
from itertools import chain
import pandas as pd
from tqdm import tqdm
import argparse
import os
import subprocess
import csv

# -------------------------------------------------- GLOBALS -------------------------------------------------- #

CHUNKSIZE = 100000
variables = set()
funcs = set()
vocab = set()

op_before = {
    "Python": {'=', '+=', '-=', '*=', '/=', '//=', '%=', '&=', '|=', '^=', '>>=', '<<=', '**='},
    "Java": {'=', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '>>=', '<<=', '>>>=', '++', '--'},
    "C++": {'=', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '>>=', '<<=', '>>>=', '++', '--'}
}

op_after = {
    "Python": {'for', 'while', 'in', ','},
    "Java": {'int', 'float', 'double', 'String', 'char', 'for', 'while', 'new'},
    "C++": {'int', 'float', 'double', 'string', 'char', 'for', 'while', '*', '&', 'new'}
}

op_func = {
    "Python": {'def', 'class'},
    "Java": {'public', 'private', 'protected', 'static', 'final', 'abstract', 'void', 'int', 'double', 'float',
             'String'},
    "C++": {'public', 'private', 'protected', 'static', 'final', 'virtual', 'void', 'int', 'double', 'float', 'string'}
}

exclude = {
    "Python": {
        'and', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'exec', 'finally',
        'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'not', 'or', 'pass', 'print', 'raise',
        'return', 'try', 'while', 'Data', 'Float', 'Int', 'Numeric', 'Oxphys', 'array', 'close', 'float', 'int',
        'input', 'open', 'range', 'str', 'type', 'write', 'zeros', 'acos', 'asin', 'atan', 'cos', 'e', 'exp',
        'fabs', 'floor', 'log', 'log10', 'pi', 'pow', 'sin', 'sqrt', 'tan', 'append', 'count', 'extend', 'index',
        'insert', 'pop', 'remove', '+', '-', '*', '/', '//', '%', '**', '<<', '>>', '&', '|', '^', '~', '<', '>', '<=',
        '>=', '==', '!=', '<>', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '>>=', '<<=', '**=', '//=', '{', '}',
        '[', ']', '(', ')', '.', ',', ':', '@', '=', ';', '+=', '-=', '*=', '/=', '//=', '%=', '&=', '|=', '^=',
        '>>=', '<<=', 'None', 'True', 'False', 'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'chr', 'complex', 'dict',
        'dir', 'divmod', 'enumerate', 'eval', 'filter', 'format', 'hex', 'id', 'len', 'list', 'map', 'max', 'min',
        'next', 'object', 'oct', 'ord', 'pow', 'repr', 'round', 'set', 'slice', 'sorted', 'sum', 'tuple', 'zip',
        'Exception', 'StopIteration', 'SystemExit', 'StandardError', 'ArithmeticError', 'OverflowError'
    },
    "Java": {
        'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char', 'class', 'const', 'continue',
        'default', 'do', 'double', 'else', 'enum', 'extends', 'final', 'finally', 'float', 'for', 'goto', 'if',
        'implements', 'import', 'instanceof', 'int', 'interface', 'long', 'native', 'new', 'package', 'private',
        'protected', 'public', 'return', 'short', 'static', 'strictfp', 'super', 'switch', 'synchronized', 'this',
        'throw', 'throws', 'transient', 'try', 'void', 'volatile', 'while', 'true', 'false', 'null', '+', '-', '*',
        '/', '%', '<<', '>>', '&', '|', '^', '~', '<', '>', '<=', '>=', '==', '!=', '+=', '-=', '*=', '/=', '%=', '&=',
        '|=',
        '^=', '>>=', '<<=', '{', '}', '[', ']', '(', ')', '.', ',', ':', '@', '=', ';', '+=', '-=', '*=', '/=',
        '%=', '&=', '|=', '^=', '>>=', '<<=', 'System', 'String', 'Integer', 'Double', 'Math', 'Object', 'Class',
        'Exception', 'Arrays', 'List', 'println', 'print', 'equals', 'length', 'hashCode', 'getClass', 'toString',
        'int', 'float', 'double', 'String', 'char', 'for', 'while', 'new', 'public', 'private', 'protected', 'static',
        'final', 'abstract', 'void', 'int', 'double', 'float',
        'String', '=', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '>>=', '<<=', '>>>=', '++', '--'
    },
    "C++": {
        'and', 'and_eq', 'asm', 'auto', 'bitand', 'bitor', 'bool', 'break', 'case', 'catch', 'char', 'class',
        'compl', 'const', 'const_cast', 'continue', 'default', 'delete', 'do', 'double', 'dynamic_cast', 'else',
        'enum', 'explicit', 'export', 'extern', 'false', 'float', 'for', 'friend', 'goto', 'if', 'inline', 'int',
        'long', 'mutable', 'namespace', 'new', 'not', 'not_eq', 'operator', 'or', 'or_eq', 'private', 'protected',
        'public', 'register', 'reinterpret_cast', 'return', 'short', 'signed', 'sizeof', 'static', 'static_cast',
        'struct', 'switch', 'template', 'this', 'throw', 'true', 'try', 'typedef', 'typeid', 'typename', 'union',
        'unsigned', 'using', 'virtual', 'void', 'volatile', 'wchar_t', 'while', 'xor', 'xor_eq', '+', '-', '*', '/',
        '%', '<<', '>>', '&', '|', '^', '~', '<', '>', '<=', '>=', '==', '!=', '+=', '-=', '*=', '/=', '%=', '&=', '|=',
        '^=', '>>=', '{', '}', '[', ']', '(', ')', '.', ',', ':', '@', '=', ';', '+=', '-=', '*=', '/=',
        '%=', '&=', '|=', '^=', '>>=', 'std', 'string', 'cout', 'cin', 'endl', 'vector', 'map', 'set', 'printf',
        'scanf', 'gets', 'puts', 'getchar', 'putchar', 'public', 'private', 'protected', 'static', 'final', 'virtual',
        'void', 'int', 'double', 'float', 'string',
        'int', 'float', 'double', 'string', 'char', 'for', 'while', '*', '&', 'new', '=', '+=', '-=', '*=', '/=', '%=',
        '&=', '|=', '^=', '>>=', '<<=', '>>>=', '++', '--'
    }
}

comments = {
    "Python": ('"""', "'''", '#'),
    "Java": ('//', '/*', '*/'),
    "C++": ('//', '/*', '*/')
}


# ------------------------------------------------- FUNCTIONS ------------------------------------------------- #


def tokenize(file):
    print(f'Tokenizing...')
    total_lines = sum(1 for _ in open(file))
    with open(file) as f:
        csv_writer = csv.writer(open(f'{file.split(".")[0]}_clean.csv', 'w'), delimiter=',')
        csv_writer.writerow(['id', 'tokens'])
        for line in tqdm(f, total=total_lines):
            tokens = line.strip().split('\t')
            csv_writer.writerow([tokens[0].split('/')[-1].split('.')[0], tokens[1:]])

    gc.collect()


def rm_comments(tokens):
    tokens = [token for token in tokens if
              not token.startswith(comments[lang]) or token.endswith(comments[lang])]
    return tokens


def rm_variables_and_func(tokens):
    for i in range(len(tokens)):
        if tokens[i] in op_before[lang]:
            if tokens[i - 1] not in variables and tokens[i - 1] not in exclude[lang]:
                variables.add(tokens[i - 1])
        elif tokens[i] in op_after[lang]:
            if lang in ["Java", "C++"]:
                if tokens[i + 2] not in variables and tokens[i + 2] not in exclude[lang]:
                    variables.add(tokens[i + 2])
            if tokens[i + 1] not in variables and tokens[i + 1] not in exclude[lang]:
                variables.add(tokens[i + 1])
        elif tokens[i] in op_func[lang]:
            if tokens[i + 1] not in funcs and tokens[i + 1] not in exclude[lang]:
                funcs.add(tokens[i + 1])

    tokens = [token if token not in variables else 'VAR' for token in tokens]
    tokens = [token if token not in funcs else 'FUNC' for token in tokens]
    return tokens


def update_vocab(tokens):
    if not char:
        for token in tokens:
            if token not in vocab:
                vocab.add(token)
    else:
        for c in ''.join(tokens):
            if c not in vocab:
                vocab.add(c)


def process_file(fp):
    print('Processing...')
    df = pd.read_csv(fp)
    df['tokens'] = df['tokens'].apply(lambda x: literal_eval(x))
    tokens = list(chain.from_iterable(df['tokens']))
    tokens = rm_comments(tokens)
    if not var:
        tokens = rm_variables_and_func(tokens)

    with open(fp.replace('.csv', f'_tokens.txt'), 'w') as f:
        if not char:
            for token in tokens:
                f.write(f'{token}\n')
        else:
            for c in ''.join(tokens):
                f.write(f'{c}\n')
    with open(fp.replace('.csv', f'_vocab.txt'), 'w') as f:
        if not char:
            for token in set(tokens):
                f.write(f'{token}\n')
        else:
            for c in set(''.join(tokens)):
                f.write(f'{c}\n')


def process_file_chunk(fp, num_lines):
    print('Processing in chunks...')
    for i, df in tqdm(enumerate(pd.read_csv(fp, chunksize=CHUNKSIZE)),
                      total=num_lines // CHUNKSIZE + 1):
        df['tokens'] = df['tokens'].apply(lambda x: literal_eval(x))
        tokens = list(chain.from_iterable(df['tokens']))
        tokens = rm_comments(tokens)
        if not var:
            tokens = rm_variables_and_func(tokens)

        mode = 'a' if i != 0 else 'w'
        with open(fp.replace('.csv', f'_tokens.txt'), mode) as f:
            if not char:
                for token in tokens:
                    f.write(f'{token}\n')
            else:
                for c in ''.join(tokens):
                    f.write(f'{c}\n')

        update_vocab(tokens)

    with open(fp.replace('.csv', f'_vocab.txt'), 'w') as f:
        for token in vocab:
            f.write(f'{token}\n')


# -------------------------------------------------- MAIN -------------------------------------------------- #


def main():
    if os.path.isfile(input_):  # Single file
        tokenize(input_)
        fp = input_.split('.')[0] + '_clean.csv'
        num_lines = int(subprocess.check_output(f"wc -l {fp}", shell=True).split()[0]) - 1
        if num_lines > CHUNKSIZE:
            process_file_chunk(fp, num_lines)
        else:
            process_file(fp)
    else:
        for root, dirs, files in os.walk(input_):
            for file in files:
                if file.endswith(".tsv"):
                    print(file)
                    tokenize(os.path.join(root, file))
                    fp = os.path.join(root, file).split('.')[0] + '_clean.csv'
                    num_lines = int(subprocess.check_output(f"wc -l {fp}", shell=True).split()[0]) - 1
                    if num_lines > CHUNKSIZE:
                        process_file_chunk(fp, num_lines)
                    else:
                        process_file(fp)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '--i', type=str, help='Directory or CSV File', required=True)
    parser.add_argument('--lang', '--l', type=str, help='Language: Java, Python, C++', required=True)
    parser.add_argument('--char', '--c', action=argparse.BooleanOptionalAction, help='Character-level tokenization',
                        default=False)
    parser.add_argument('--var', '--v', action=argparse.BooleanOptionalAction, help='Keep variables', default=False)
    args = parser.parse_args()
    input_ = args.input
    lang = args.lang
    char = args.char
    var = args.var

    main()

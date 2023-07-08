'''
Clean computer language code from comments, strings, and other non-code elements.
'''
import gc
# -------------------------------------------------- IMPORTS -------------------------------------------------- #

# External
from tqdm import tqdm
import argparse
import os
import csv

# -------------------------------------------------- GLOBALS -------------------------------------------------- #

variables = set()
funcs = set()
comment_set = set()
string_set = set()
number_set = set()

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
        'Exception', 'StopIteration', 'SystemExit', 'StandardError', 'ArithmeticError', 'OverflowError', 'main',
        '#VAR#', '#FUNC#', '#NUM#', '#STR#', "#COMMENTS#", "#NEWLINE#", "#INDENT#", "#DEDENT#"
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
        'String', '=', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '>>=', '<<=', '>>>=', '++', '--', 'main',
        '#VAR#', '#FUNC#', '#NUM#', '#STR#', "#COMMENTS#", "#NEWLINE#", "#INDENT#", "#DEDENT#"
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
        '&=', '|=', '^=', '>>=', '<<=', '>>>=', '++', '--', 'main', '#VAR#', '#FUNC#', '#NUM#', '#STR#', "#COMMENTS#",
        "#NEWLINE#", "#INDENT#", "#DEDENT#"
    }
}

comments = {
    "Python": ('"""', "'''", '#'),
    "Java": ('//', '/*', '*/'),
    "C++": ('//', '/*', '*/')
}


# ------------------------------------------------- FUNCTIONS ------------------------------------------------- #

def rm_comments(tokens):
    if debug:
        for i in range(len(tokens)):
            if (tokens[i].startswith(comments[lang]) or tokens[i].endswith(comments[lang])) and tokens[i] not in exclude[
                lang]:
                comment_set.add(tokens[i])
                tokens[i] = "#COMMENTS#"
    else:
        tokens = [
            "#COMMENTS#" if (token.startswith(comments[lang]) or token.endswith(comments[lang])) and token not in
                            exclude[
                                lang] else token for token in
            tokens]

    return tokens


def rm_strings(tokens):
    if debug:
        for i in range(len(tokens)):
            if (tokens[i].startswith(('"', "'", "f'", 'f"')) or tokens[i].endswith(('"', "'"))) and tokens[i] not in \
                    exclude[lang]:
                string_set.add(tokens[i])
                tokens[i] = "#STR#"
    else:
        tokens = ["#STR#" if (token.startswith(('"', "'")) or token.endswith(('"', "'"))) and token not in exclude[
            lang] else token for token in tokens]

    return tokens


def rm_numbers(tokens):
    if debug:
        for i in range(len(tokens)):
            if tokens[i].isdigit() and tokens[i] not in exclude[lang]:
                number_set.add(tokens[i])
                tokens[i] = "#NUM#"
    else:
        tokens = ["#NUM#" if token.isdigit() and token not in exclude[lang] else token for token in tokens]

    return tokens


def rm_variables_and_func(tokens):
    for i in range(len(tokens)):
        if tokens[i] in op_before[lang] and i - 1 >= 0:
            if tokens[i - 1] not in variables and tokens[i - 1] not in exclude[lang]:
                variables.add(tokens[i - 1])
        elif tokens[i] in op_after[lang] and i + 1 < len(tokens):
            if lang in ["Java", "C++"] and i + 2 < len(tokens):
                if tokens[i + 2] not in variables and tokens[i + 2] not in exclude[lang]:
                    variables.add(tokens[i + 2])
            if tokens[i + 1] not in variables and tokens[i + 1] not in exclude[lang]:
                variables.add(tokens[i + 1])
        elif tokens[i] in op_func[lang]:
            if tokens[i + 1] not in funcs and tokens[i + 1] not in exclude[lang]:
                funcs.add(tokens[i + 1])

    tokens = [token if token not in funcs else '#FUNC#' for token in tokens]
    tokens = [token if token not in variables else '#VAR#' for token in tokens]
    return tokens


def process_file(file):
    output_dir = f'clean{"_STR" if not string else ""}{"_NUM" if not number else ""}{"_VAR" if not var else ""}{"_COMMENTS" if not comments_ else ""}'
    total_lines = sum(1 for _ in open(file))
    with open(file) as f:
        if not os.path.exists(os.path.join(os.path.dirname(file), output_dir)):
            os.makedirs(os.path.join(os.path.dirname(file), output_dir))
        csv_writer = csv.writer(
            open(os.path.join(os.path.dirname(file), output_dir, f'{os.path.basename(file).split(".")[0]}.csv'), 'w', ),
            delimiter=',')
        csv_writer.writerow(['id', 'tokens'])
        for line in tqdm(f, total=total_lines):
            tokens = line.strip().split('\t')
            id = tokens[0].split('/')[-1].split('.')[0]
            tokens = tokens[1:]
            if not comments_:
                tokens = rm_comments(tokens)
            if not string:
                tokens = rm_strings(tokens)
            if not number:
                tokens = rm_numbers(tokens)
            if not var:
                tokens = rm_variables_and_func(tokens)

            csv_writer.writerow([id, tokens])


# -------------------------------------------------- MAIN -------------------------------------------------- #


def main():
    print(f'Cleaning {lang}:')
    if os.path.isfile(input_):  # Single file
        print(f'Processing {input_}...')
        process_file(input_)
    else:
        for root, dirs, files in os.walk(input_):
            for file in files:
                if file.endswith(".tsv"):
                    print(f'Processing {input_}...')
                    process_file(os.path.join(root, file))

    if debug:
        output_dir = f'clean{"_STR" if not string else ""}{"_NUM" if not number else ""}{"_VAR" if not var else ""}{"_COMMENTS" if not comments_ else ""}'
        with open(os.path.join(os.path.dirname(input_), output_dir, 'variables.txt'), 'w') as f:
            for i in variables:
                f.write(i + "\n")

        with open(os.path.join(os.path.dirname(input_), output_dir, 'funcs.txt'), 'w') as f:
            for i in funcs:
                f.write(i + "\n")

        with open(os.path.join(os.path.dirname(input_), output_dir, 'comments.txt'), 'w') as f:
            for i in comment_set:
                f.write(str(i) + "\n")

        with open(os.path.join(os.path.dirname(input_), output_dir, 'numbers.txt'), 'w') as f:
            for i in number_set:
                f.write(str(i) + "\n")

        with open(os.path.join(os.path.dirname(input_), output_dir, 'strings.txt'), 'w') as f:
            for i in string_set:
                f.write(str(i) + "\n")


# -------------------------------------------------- CLI -------------------------------------------------- #


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '--i', type=str, help='Directory or CSV File', required=True)
    parser.add_argument('--lang', '--l', type=str, help='Language: Java, Python, C++', required=True)
    parser.add_argument('--debug', '--d', action=argparse.BooleanOptionalAction,
                        help='Debug, get replacements details in output file', default=False)

    parser.add_argument('--var', '--v', action=argparse.BooleanOptionalAction, help='Keep variables', default=False)
    parser.add_argument('--number', '--num', action=argparse.BooleanOptionalAction, help='Keep numbers', default=False)
    parser.add_argument('--comments', '--com', action=argparse.BooleanOptionalAction, help='Keep comments',
                        default=False)
    parser.add_argument('--string', '--s', action=argparse.BooleanOptionalAction, help='Keep strings', default=False)

    args = parser.parse_args()
    input_ = args.input
    lang = args.lang
    debug = args.debug

    var = args.var
    number = args.number
    comments_ = args.comments
    string = args.string

    main()

import os
import re
from sys import argv

def line_length(line: str):
    return len(line) > 79


def indentation_check(line: str):
    num_spaces = 0
    for i, ch in enumerate(line):
        if ch != ' ':
            num_spaces = line.count(' ', 0, i)
            break

    if num_spaces % 4:
        return 1
    else:
        return 0


def check_semicolon(line: str):
    i = 0
    while len(line) > i:
        if line[i] == '"':  # think how to avoid repeating this code
            i += 1
            while line[i] != '"':
                i += 1
                if line[i] == '\\':
                    i += 2
        if line[i] == "'":  # think how to avoid repeating this code
            i += 1
            while line[i] != "'":
                i += 1
                if line[i] == '\\':
                    i += 2
        if line[i] == '#':
            return 0
        if line[i] == ';':
            return 1
        i += 1
    return 0


def cmt_space(line: str):
    if '#' in line and not line.startswith('#'):
        index = line.index('#')
        return line[index - 2: index] != '  '


def find_todo(line: str):
    if '#' in line:
        index = line.index('#')
        return 'todo' in line[index:].lower()


def spaces(line: str, x_line: int, path: str):

    if line.startswith('class '):
        if not re.match(r'class \b', line):
            print(f'{path}: Line {x_line}: S007 Too many spaces after "class"')
    elif line.startswith('def '):
        if not re.match(r'def \b', line):
            print(f'{path}: Line {x_line}: S007 Too many spaces after "def"')
    
def camel_case(line: str, x_line: int, path: str):
    if line.startswith('class '):
        template = line.split()
        match = re.match(r'\w+', template[1])
        if template[1][0] != template[1][0].upper():
            print(f"{path}: Line {x_line}: S008 Class name '{match.group()}' should use CamelCase")
        if '_' in template[1]:
            print(f"{path}: Line {x_line}: S008 Class name '{match.group()}' should use CamelCase")

def snake_case(line: str, x_line: int, path: str):
    if line.startswith('def '):
        template = line.split()
        match = re.match(r'\w+', template[1])
        if re.match(r'[a-z0-9_]+[(:]', template[1]):
            pass
        else:
            print(f"{path}: Line {x_line}: S009 Function name '{match.group()}' should use snake_case")

def analyzer(file_path):
    count_blanks = 0
    with open(file_path) as file:
        code_list = file.read().splitlines()

    for x_line, line in enumerate(code_list, start=1):
        if line_length(line):
            print(f'{file_path}: Line {x_line}: S001 Too long')
        if indentation_check(line):
            print(f'{file_path}: Line {x_line}: S002 Indentation is not a multiple of four')
        if check_semicolon(line):
            print(f'{file_path}: Line {x_line}: S003 Unnecessary semicolon')
        if cmt_space(line):
            print(f'{file_path}: Line {x_line}: S004 At least two spaces required before inline comments')
        if find_todo(line):
            print(f'{file_path}: Line {x_line}: S005 TODO found')

        # S006 Finding blanks
        if not line or all(' ' == i for i in line):
            count_blanks += 1
        elif count_blanks > 2:
            print(f'{file_path}: Line {x_line}: S006 More than two blank lines used before this line')
            count_blanks = 0
        else:
            count_blanks = 0
        spaces(line.lstrip(), x_line, file_path)
        camel_case(line.lstrip(), x_line, file_path)
        snake_case(line.lstrip(), x_line, file_path)


if not os.access(argv[1], os.F_OK):
    print("There is no such file or directory")
if os.path.isdir(argv[1]):
    for root, dirs, files in os.walk(argv[1], topdown=True):
        for name in files:
            file_path = os.path.join(root, name)
            analyzer(file_path)
else:
    analyzer(argv[1])

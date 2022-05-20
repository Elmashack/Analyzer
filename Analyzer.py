import os
import re
import ast
from sys import argv
from typing import Any


def tree_manager(func):

    def wrapper(line):
        line = line.lstrip()
        if not line.startswith('def '):
            return False
        line += '\n\tpass'
        node = ast.parse(line)
        return func(node)
    
    return wrapper


def line_length(line: str):  # S001 long line
    return len(line) > 79


def indentation_check(line: str):  # S002 Indentation error
    num_spaces = 0
    for i, ch in enumerate(line):
        if ch != ' ':
            num_spaces = line.count(' ', 0, i)
            break

    if num_spaces % 4:
        return 1
    else:
        return 0


def check_semicolon(line: str):  # S003 Unnessecary semicolon
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


def cmt_space(line: str):  # S004 space before comment
    if '#' in line and not line.startswith('#'):
        index = line.index('#')
        return line[index - 2: index] != '  '


def find_todo(line: str):  # S005 TODO found
    if '#' in line:
        index = line.index('#')
        return 'todo' in line[index:].lower()


def spaces(line: str, x_line: int, path: str):  # S007 spaces after class/def

    if line.startswith('class '):
        if not re.match(r'class \b', line):
            print(f'{path}: Line {x_line}: S007 Too many spaces after "class"')
    elif line.startswith('def '):
        if not re.match(r'def \b', line):
            print(f'{path}: Line {x_line}: S007 Too many spaces after "def"')


def camel_case(line: str, x_line: int, path: str):  #S008 CamelCase in Class
    if line.startswith('class '):
        template = line.split()
        match = re.match(r'\w+', template[1])
        if template[1][0] != template[1][0].upper():
            print(f"{path}: Line {x_line}: S008 Class name '{match.group()}' should use CamelCase")
        if '_' in template[1]:
            print(f"{path}: Line {x_line}: S008 Class name '{match.group()}' should use CamelCase")


def snake_case(line: str, x_line: int, path: str):  # S009 snake_case in function name  
    if line.startswith('def '):
        template = line.split()
        match = re.match(r'\w+', template[1])
        if re.match(r'[a-z\d_]+[(:]', template[1]):
            pass
        else:
            print(f"{path}: Line {x_line}: S009 Function name '{match.group()}' should use snake_case")
        

@tree_manager
def arg_name(node):  # S010 snake_case in argument name
    body = node.body[0].args.args
    args = [a.arg for a in body]
    for arg in args:
        if re.search(r'[A-Z]+', arg):
            return arg
    return False


def var_name(line):  # S011 Variable name in snake_case
    try:
        node = ast.parse(line.lstrip())
        elem = node.body[0]
        if isinstance(elem, ast.Assign):
            if isinstance(elem.targets[0], ast.Attribute):
                var = elem.targets[0].attr
            else:
                var = elem.targets[0].id
            if re.search(r'[A-Z]+', var):
                return var
        return False
    except Exception:
        return False


@tree_manager
def mutable_arg(node):  # S012 Default arg is mutable
    args_type = [isinstance(df, (ast.List, ast.Dict, ast.Set)) for df in node.body[0].args.defaults]
    if any(args_type):
        return True
    return False
        

def analyzer(file_path: str):
    count_blanks = 0
    with open(file_path, "r") as file:
        code_list = file.read().splitlines()
        file.seek(0)

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
        if arg_name(line):
            print(f'{file_path}: Line {x_line}: S010 Argument name "{arg_name(line)}" should be snake_case')
        if var_name(line):
            print(f'{file_path}: Line {x_line}: S011 Variable "{var_name(line)}" in function should be snake_case')
        if mutable_arg(line):
            print(f'{file_path}: Line {x_line}: S012 Default argument value is mutable')


if __name__ == "__main__":
    file_path = []
    if not os.access(argv[1], os.F_OK):
        print("There is no such file or directory")
    if os.path.isdir(argv[1]):
        for root, dirs, files in os.walk(argv[1], topdown=False):
            for name in files:
                file_path.append(os.path.join(root, name))
        file_path.sort()
        for path in file_path:
            analyzer(path)
    else:
        analyzer(argv[1])

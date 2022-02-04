path = input()

code = {}



def strip_comment(line):
    return line.split("#")[0].rstrip()


def strip_code(line):
    index = line.index("#") if "#" in line else len(line)
    return line[index:len(line)]


def length_err(line):
    return len(line) > 79


def indentation_err(line):
    return (len(line) - len(line.lstrip(" "))) % 4 != 0


def semicolon_err(line):
    line = strip_comment(line).strip()
    return line.endswith(";")


def comment_err(line):
    if "#" in line:
        line = line.lstrip()
        index = line.index("#")
        if index > 0:
            try:
                if line[index - 1] != " " or line[index - 2] != " ":
                    return True
            except:
                pass
    return False


def todo_found(line):
    line = strip_code(line).lower()
    if len(line) > 0 and " todo" in line:
        return True
    else:
        return False


def blank_lines_err(i, line):
    if i >= 4:
        if len(line) > 0 and len(code.get(i - 1)) == 0 and len(code.get(i - 2)) == 0 and len(code.get(i - 3)) == 0:
            return True
    return False

with open(path, 'r') as file:
    for i, line in enumerate(file, 1):
        if length_err(line):
            print(f"Line {i}: S001 Too long")
        if indentation_err(line):
            print(f"Line {i}: S002 ndentation is not a multiple of four")
        if semicolon_err(line):
            print(f"Line {i}: S003 Unnecessery semicolon")
        if comment_err(line):
            print(f"Line {i}: S004 At least two spaces required before inline comments")
        if todo_found(line):
            print(f"Line {i}: S005 TODO found")
        if blank_lines_err(i, line):
            print(f"Line {i}: S006 More than two blank lines used before this line")

import os
import sys

# def skip_quotes(line, i):
def fullspace_line(line):
    for i in range(len(line) - 1):
        if line[i] != ' ':
            return 0
    return 1

class Analyzer:

    def __init__(self) -> None:
        self.passed_line = []
        self.args = sys.argv
        # file_path = args[1]
     
        if not os.access(self.args[1], os.F_OK):   # if input file exists 
            print("There is no such file or directory")
        if os.path.isdir(self.args[1]):
            files_dir = os.listdir(self.args[1])
            files_dir.sort()
            for file_path in files_dir:
                self.main_func(file_path)
        else:
            file_path = self.args[1]
            self.main_func(file_path)


    def main_func(self, file_path):
        abspath = os.path.abspath(file_path)
        x_line = 0   
        count_n = 0          
        with open(abspath, "r", encoding='utf-8') as file:
            for line in file:
                self.passed_line.append(line)
                x_line += 1
                if len(line) > 79:
                    print(f"{abspath}: Line {x_line}: S001 Too long")
                if self.indentation_check(self.passed_line):
                    print(f"{abspath}: Line {x_line}: S002 Indentation is not a multiple of four")
                if self.check_semicolon(line):
                    print(f"{abspath}: Line {x_line}: S003 Unnecessary semicolon")
                self.space_todo_of_comment(line, x_line, abspath)
                if line == "\n" or fullspace_line(line):
                    count_n += 1
                else:
                    count_n = 0
                if count_n > 2:
                    print(f"{abspath}: Line {x_line}: S006 More than two blank lines used before this line")

    def indentation_check(self, passed_line):
        num_spaces = 0
        # colon = 0
        for line in passed_line:
            flag = 1
            for i, ch in enumerate(line):
                if ch != ' ' and flag:
                    num_spaces = line.count(' ', 0, i)
                    flag = 0
                # if ch == ':':
                #     colon = 1
                
        if num_spaces % 4:
            return 1
        # elif num_spaces > 0 and not colon:
        #     return 1
        else: 
            return 0

    def check_semicolon(self, line):

        i = 0
        while len(line) > i:
            if line[i] == '"': # think how to avoid repeating this code
                i += 1 
                while line[i] != '"':
                    i += 1
                    if line[i] == '\\':
                            i += 2
            if line[i] == "'": # think how to avoid repeating this code
                i += 1 
                while line[i] != "'":
                    i += 1
                    if line[i] == '\\':
                        i += 2
            if line[i] == '#':
                break
            if line[i] == ';':
                return 1
            i += 1
        return 0

    def space_todo_of_comment(self, line, x_line, abspath):
        i = 0
        while len(line) > i:
            if line[i] == '"': # think how to avoid repeating this code
                i += 1 
                while line[i] != '"':
                    i += 1
                    if line[i] == '\\':
                        i += 2
            if line[i] == "'": # think how to avoid repeating this code
                i += 1 
                while line[i] != "'":
                    i += 1
                    if line[i] == '\\':
                        i += 2
            if line[i] == '#':
                if line[i - 1] != ' ' or line[i - 2] != ' ':
                    print(f"{abspath}: Line {x_line}: S004 At least two spaces required before inline comments")
                if line.lower().find('todo', i) >= 0: 
                    print(f"{abspath}: Line {x_line}: S005 TODO found")
                break
            i += 1


    
Analyzer()
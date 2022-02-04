print('hello')
 print('hello')
  print('hello')
    print('hello')
      print('hello')
        print('hello')

print('hello')
print('hello');
print('hello');;;
print('hello');  # hello
# hello hello hello;
greeting = 'hello;'
print('hello')  # ;


class Analyzer:

    def __init__(self) -> None:
        self.file_path = input()
        self.x_line = 0
        with open(self.file_path, "r", encoding='utf-8') as file:
            for line in file:
                self.x_line += 1
                if len(line) > 79:
                    print(f"Line {self.x_line}: S001 Too ;;long")
                if self.indentation_check(self):
                    print(f"Line {self.x_line}: S002  indentation is not a multiple of four")

    
    def indentation_check(self, line):
        for i, ch in enumerate(line):
            if ch != ' ':
                num_spaces = line.count(' ', 0, i)
        if num_spaces % 4:
            return 1
        else: 
            return 0

print('What\'s #  your name?')  # reading todo ;an input

name = input()
print(f'Hello, {name}'); # here is an obvious todo comment: this prints a greeting with a name


very_big_number = 11_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000
print(very_big_number)



def some_fun():
    print('NO TODO HERE;;')
    pass # Todo something

import random


class TicToe:

    def __init__(self, player1, player2) -> None:
        self.player1 = player1
        self.player2 = player2
        self.mark = None
        self.y = 0
        self.x = 0
        self.my_map = [list(' ' * 3) for _ in range(3)]
        self.op_mark = None

    def opposite_mark(self):
        if self.mark == 'X':
            self.op_mark = 'O'
        else:
            self.op_mark = 'X'

    def if_draw(self):
        for row in self.my_map:
            if any([i == ' ' for i in row]):
                return 0
        return 1

    def define_mark(self):
        x_mark = 0
        o_mark = 0
        for row in self.my_map:
            x_mark += row.count('X')
            o_mark += row.count('O')
        return 'X' if x_mark == o_mark else 'O'

    def who_win(self, sign):
        # Horizontal win
        for row in self.my_map:
            if all([i == sign for i in row]):
                return 1

        # Vertical win
        for x in range(3):
            if all([self.my_map[y][x] == sign for y in range(3)]):
                return 1

        # First diagonal win
        if (self.my_map[0][0] == sign and
                self.my_map[1][1] == sign and self.my_map[2][2] == sign):
            return 1
        # Second diagonal win
        elif (self.my_map[0][2] == sign and
              self.my_map[1][1] == sign and self.my_map[2][0] == sign):
            return 1
        else:
            return 0

    def user_move(self):
        while True:
            try:
                y, x = map(int, input('Enter the coordinates: > ').split())
            except ValueError:
                print('You should enter numbers!')
                continue
            else:
                if x not in range(1, 4) or y not in range(1, 4):
                    print("Coordinates should be from 1 to 3!")
                    continue
                elif self.my_map[y - 1][x - 1] == ' ':
                    self.y, self.x = y, x
                    return
                else:
                    print("This cell is occupied! Choose another one!")

    def ai_move(self):
        print('Making move level "easy"')
        while True:
            y = random.randint(1, 3)
            x = random.randint(1, 3)
            if self.my_map[y - 1][x - 1] == ' ':
                self.y, self.x = y, x
                return

    def start_game(self):
        print(self)  # drawing the map
        while True:
            self.mark = self.define_mark()
            if self.player1 == 'user' and self.mark == 'X' or self.player2 == 'user' and self.mark == 'O':
                self.user_move()
            else:
                self.ai_move()
            self.my_map[self.y - 1][self.x - 1] = self.mark
            print(self)  # updating the map
            if self.who_win(self.mark):
                print(f"{self.mark} wins")
                return
            elif self.if_draw():
                print('Draw')
                return

    def __str__(self) -> str:
        cells = '---------\n'
        for i in range(3):
            cells += f"| {' '.join(self.my_map[i])} |\n"
        cells += '---------\n'
        return cells


class MediumLevel(TicToe):

    def opposite_mark(self):
        if self.mark == 'X':
            self.op_mark = 'O'
        else:
            self.op_mark = 'X'

    def check_move(self, sign):
        y = 0
        x = 0
        diagonal_cells = [self.my_map[i][i] for i in range(3)]
        diagonal_cells1 = [self.my_map[i][2 - i] for i in range(3)]
        vertical_cells = [[row[i] for row in self.my_map] for i in range(3)]

        # checking the horizontal potential win or lose
        for row in self.my_map:
            y += 1
            if row.count(sign) == 2 and row.count(' ') == 1:
                x = row.index(' ')
                self.y, self.x = y, x + 1
                return 1
        # checking the vertical potential win or lose
        for row in vertical_cells:
            x += 1
            if row.count(sign) == 2 and row.count(' ') == 1:
                y = row.index(' ')
                self.y, self.x = y + 1, x
                return 1
        # checking the diagonal potential win or lose
        if diagonal_cells.count(sign) == 2 and diagonal_cells.count(' ') == 1:
            y = diagonal_cells.index(' ')
            self.y, self.x = y + 1, y + 1
            return 1
        if diagonal_cells1.count(sign) == 2 and diagonal_cells.count(' ') == 1:
            y = diagonal_cells1.index(' ')
            self.y, self.x = y + 1, 3 - y
            return 1
        return 0

    def ai_move(self):
        print('Making move level "medium"')
        self.opposite_mark()
        if self.check_move(self.mark):
            return
        elif self.check_move(self.op_mark):
            return
        else:
            while True:
                y = random.randint(1, 3)
                x = random.randint(1, 3)
                if self.my_map[y - 1][x - 1] == ' ':
                    self.y, self.x = y, x
                    return


class HardLevel(TicToe):

    # using the minimax algorithm

    # predicting the scenario of every move pc can make
    def max_score(self):
        max_v = -2

        y = None
        x = None

        if self.who_win(self.mark):
            return 1
        elif self.who_win(self.op_mark):
            return -1
        elif self.if_draw():
            return 0

        for i in range(3):
            for j in range(3):
                if self.my_map[i][j] == ' ':
                    self.my_map[i][j] = self.mark
                    m = self.min_score()
                    if m > max_v:
                        max_v = m
                        y = i + 1
                        x = j + 1
                    self.my_map[i][j] = ' '
        self.y, self.x = y, x
        return max_v

    # predicting the scenario of every move opponent can make
    def min_score(self):
        min_v = 2

        y = None
        x = None
        if self.who_win(self.mark):
            return 1
        elif self.who_win(self.op_mark):
            return -1
        elif self.if_draw():
            return 0

        for i in range(3):
            for j in range(3):
                if self.my_map[i][j] == ' ':
                    self.my_map[i][j] = self.op_mark
                    m = self.max_score()
                    if m < min_v:
                        min_v = m
                    self.my_map[i][j] = ' '
        return min_v

    def ai_move(self):
        self.opposite_mark()
        print('Making move level "hard"')
        self.max_score()


class MenuBar:

    def menu_bar(self):
        cmd = []
        while True:
            try:
                cmd = input("Input command: > ").split()
            except IndexError:
                print("Bad parameters!")
            else:
                if cmd[0] == "exit":
                    exit()
                elif cmd[0] == "start" and len(cmd) != 3:
                    print("Bad parameters!")
                    continue
                elif cmd[0] == 'start' and 'medium' in cmd:
                    MediumLevel(cmd[1], cmd[2]).start_game()
                elif cmd[0] == 'start' and 'hard' in cmd:
                    HardLevel(cmd[1], cmd[2]).start_game()
                else:
                    TicToe(cmd[1], cmd[2]).start_game()


if __name__ == '__main__':
    play = MenuBar()
    play.menu_bar()





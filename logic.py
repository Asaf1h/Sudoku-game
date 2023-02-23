import random
from constants import *
import utils
import pygame


def sudoku_generator():
    """Function that creates sudoku board and its solution.
    the solution is meant filter out all the sudokus without an existing solution"""

    searching = True
    while searching:
        new_sudoku_board = Board()
        row_col_box_set = new_sudoku_board.reset_sets()
        new_sudoku_board.sudoku_maker(*row_col_box_set)
        board = [line.copy() for line in new_sudoku_board.board]
        comb_sets = sorted(Board.get_comb_sets(
            board), reverse=True, key=lambda cube: len(cube[0]))
        # Filters out all the non-solution sudoku
        if len(comb_sets[-1][0]) == 0:
            continue
        new_sudoku_board.solver(comb_sets)
        # Filters out all the non-solution sudoku
        if utils.find_empty(new_sudoku_board.board) == None:
            solution = [line.copy() for line in new_sudoku_board.board]
            return board, solution


class Mixin:
    """A Mixin class to help manage the Grid class and Board class get their job done."""

    @staticmethod
    def insert_num_comb(comb_sets, row, col, box_num, val):
        """Remove the user input from all the sets that links to the user input location.

         Args:
            comb_sets (list[(set{int}, row[int], col[int], box[int])]):
             Array that contains all the combinations and locations for each cube.
             .
            row (int): user row input location.
            col (int): user col input location.
            box_num (int): user box input location.
            val (int): user number input.

        Returns:
            next_comb_sets (list[(set{int}, row[int], col[int], box[int])]):
             the new sets without the number that nearby the user input.
             the array that contains all the combinations and locations for each cube.
        """
        next_comb_sets = [cube.copy() for cube in comb_sets]
        for cube in next_comb_sets:
            cube_row, cube_col, cube_box = cube[1]
            if row == cube_row or col == cube_col or box_num == cube_box:
                if val in cube[0]:
                    cube[0].remove(val)
        return next_comb_sets

    @staticmethod
    def _get_box_sets(board):
        """Extract all the numbers within each box.
        Args:
            board (list[int][int]): The sudoku board that contains all the numbers.

        Returns:
            box_sets (list[set{int}]):  all the numbers that exist in each cube.
        """
        # make 9 boxes
        box_sets = [{0} for _ in range(N)]

        for i in range(N):
            for j in range(N):
                box_num = 3 * (i // 3) + j // 3
                box_sets[box_num].update({board[i][j]})
        return box_sets

    @staticmethod
    def _get_sets(board):
        """Extract all the numbers that cannot be found in each row, col and box.

          Args:
             board (list[int][int]): Array that contains all the numbers in the current board.

         Returns:
             row_sets (list[set{int}]): all the numbers that cannot be found in each row.
             col_sets (list[set{int}]): all the numbers that cannot be found in each col.
             box_sets (list[set{int}]): all the numbers that cannot be found in each box.
         """
        num_set = set(range(1, N + 1))
        row_sets = [num_set.copy() for _ in range(N)]
        col_sets = [num_set.copy() for _ in range(N)]
        box_sets = [num_set.copy() for _ in range(N)]

        cur_row_sets = [set(row) for row in board]
        cur_col_sets = [set(map(lambda j: board[j][col_i], range(N)))
                        for col_i in range(N)]
        cur_box_sets = Mixin._get_box_sets(board)

        row_sets = [row_sets[i] - cur_row_sets[i] for i in range(N)]
        col_sets = [col_sets[i] - cur_col_sets[i] for i in range(N)]
        box_sets = [box_sets[i] - cur_box_sets[i] for i in range(N)]
        return row_sets, col_sets, box_sets

    @staticmethod
    def get_comb_sets(board):
        """Creates an array that contains in each unit set of all the user available.
         numbers for each box, and its cube position.

        Args:
            board (list[int][int]): Array that contains all the numbers in the current board.

        Returns:
            comb (set{int}): all the available numbers that can be use for each cube.
            row (int): row index position.
            col (int): col index position.
            box_num (int): box index position.
        """
        row_sets, col_sets, box_sets = Mixin._get_sets(board)
        for row in range(N):
            for col in range(N):
                if board[row][col] == 0:
                    box_num = 3 * (row // 3) + (col // 3)
                    comb = row_sets[row] & col_sets[col] & box_sets[box_num]
                    yield [comb, (row, col, box_num)]

    def valid(self, num, num_row, num_col):
        """Check for given number if there is no collision with another number on the board.

        Args:
            num (int): A given number.
            num_row (int): The number row index.
            num_col (int): The number col index.

        Returns:
             bool: True of false depends on the validation result.
        """
        if num == 0:
            return True
        # check row
        if len(self) == N:
            for i, curr_num in enumerate(self[num_row]):
                if curr_num == num and i != num_col:
                    return False

        # check column
        for row_index in range(len(self)):
            if self[row_index][num_col] == num and row_index != num_row:
                return False
        # check box
        box_row = num_row // 3
        box_col = num_col // 3
        if len(self) % 3 == 0:
            upper_box_limit = box_row * 3 + 3
        elif len(self) % 3 == 2:
            upper_box_limit = box_row * 3 + 2
        else:  # don't need to check the box if it has one line
            return True
        for i in range(box_row * 3, upper_box_limit):
            for j in range(box_col * 3, box_col * 3 + 3):
                if self[i][j] == num and (i, j) != (num_row, num_col):
                    return False
        return True


class Grid(Mixin):
    """Grid class helps to manage the sudoku game board.

    Args:
        sudoku_board (list[int][int]): Array that contains all the numbers in the current board.
        sol (list[int][int]): Array that contains all the numbers in the current board.

    Attributes:
        sudoku_board (list[int][int]): Array that contains the solution for the current current board.
        cubes (list[list[Cube object]]): initialization the cube board.
        reset (list[int][int]): the initial game board.
        sol (list[int][int]): Array that contains the solution for the current current board.
        insert (int): check if number was insert by the user.
    """

    def __init__(self, sudoku_board, sol):
        self.sudoku_board = sudoku_board
        self.init_board = [self.sudoku_board[i].copy() for i in range(N)]

        self.cubes = [[Cube(sudoku_board[i][j])
                       for j in range(N)] for i in range(N)]

        self.sol = sol
        self.insert = 0

    def reset_board(self):
        self.sudoku_board = [self.init_board[i].copy() for i in range(N)]
        self.cubes = [[Cube(self.sudoku_board[i][j])
                       for j in range(N)] for i in range(N)]

    def solver(self, comb_sets, win):
        """Recursive function that helps to solve sudoku board.

        Args:
            comb_sets (list[(set{int}, row[int], col[int], box[int])]):
            the array that contains all the combinations and locations for each cube.
            win (pygame object): helps to draw the board.

        Returns:
            box_sets (list[set{int}]):  all the numbers that exist in each cube.
        """
        win.FPS_CLOCK.tick(30)

        if len(comb_sets) == 0:
            return True
        # check if there is cube without any available num to insert
        elif len(comb_sets[-1][0]) == 0:
            return False
        cur_cube = comb_sets.pop()
        num_options = cur_cube[0]
        row, col, box_num = cur_cube[1]
        for num in num_options:
            self.sudoku_board[row][col] = num
            self.cubes[row][col].set(num)

            win.draw_board(self)
            win.draw_high_light_box(GREEN, row, col)
            pygame.display.update()
            win.draw_high_light_box(WINDOW_COLOR, row, col)
            next_comb_sets = Board.insert_num_comb(
                comb_sets, row, col, box_num, num)
            next_comb_sets = sorted(
                next_comb_sets, reverse=True, key=lambda cube: len(cube[0]))
            if self.solver(next_comb_sets, win):
                return True
            self.sudoku_board[row][col] = 0
            self.cubes[row][col].remove()

            pygame.display.update()

        return False

    def place(self, val, *pos):
        """Insert given value for given position.

        Args:
            val (int): User input.
            pos (tuple(int,int)): User input value position.

        Returns:
            bool:  return if success or not.
        """
        row, col = pos
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.sudoku_board[row][col] = val
            if Board.valid(self.sudoku_board, val, row, col):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.sudoku_board[row][col] = 0
                return False

    def _user_wrong__input_pos(self):
        """Privet function that find the next user input.

        Args:  None.

        Returns:
            i [int]: one of the user input row index.
            j [int]: one of the user input col index.
        """
        for i in range(N):
            for j in range(N):
                if self.cubes[i][j].value != 0 and not self.cubes[i][j].original:
                    return i, j

    def fix_player_set_point(self, win):
        """Function that deletes one of the user inputs.
        It helps to fix wrong user input during the solve function.

        Args:
            win (pygame object): helps to draw the board.

        Returns:  None.
        """
        row, col = self._user_wrong__input_pos()
        win.draw_high_light_box(RED, row, col)
        self.sudoku_board[row][col] = 0
        self.cubes[row][col].set(0)


class Cube:
    """Cube class helps to manage the each cube in sudoku game board.

        Args:
            value (int): Use cube value input.

        Attributes:
            value (int): cube value.
            temp (int): sketch value.
            original (bool): check if given cube is from the original board.
    """

    def __init__(self, value):
        self.value = value
        self.temp = 0
        if self.value:
            self.original = 1
        else:
            self.original = 0

    def set(self, val):
        """Insert given value to given cube."""
        self.value = val
        self.temp = 0

    def set_temp(self, val):
        """Insert Sketch value to given cube."""
        self.temp = val

    def remove(self):
        """Remove given value form given cube."""
        if not self.original:
            self.value = 0
            self.temp = 0


class Board(Mixin):
    """Board class helps to manage sudoku generation process.

        Args:  None

        Attributes:
            board (list[int][int]): Array that contains all the numbers in the current board.
    """

    def __init__(self):
        self.board = [['-'] * N for _ in range(N)]

    @staticmethod
    def reset_sets():
        """Get all the numbers that can be inserted in each row, col and box."""
        num_set = set(range(1, N + 1))
        row_sets = [num_set.copy() for _ in range(N)]
        col_sets = [num_set.copy() for _ in range(N)]
        box_sets = [num_set.copy() for _ in range(N)]
        return row_sets, col_sets, box_sets

    def _find_next_pos(self):
        """Find the next empty position"""
        for i, row in enumerate(self.board):
            for j, num in enumerate(row):
                if num == '-':
                    return i, j

    def solver(self, comb_sets):
        """Recursive function that helps to solve sudoku board.

        Args:
            comb_sets (list[(set{int}, row[int], col[int], box[int])]):
            the array that contains all the combinations and locations for each cube.

        Returns:
            bool: return True for success or false for failure
        """
        if len(comb_sets) == 0:
            return True
        # check if there is cube without any available num
        elif len(comb_sets[-1][0]) == 0:
            return False
        cur_cube = comb_sets.pop()
        num_options = cur_cube[0]
        row, col, box_num = cur_cube[1]
        # check all the possibilities for each position
        for num in num_options:
            self.board[row][col] = num
            next_comb_sets = Board.insert_num_comb(
                comb_sets, row, col, box_num, num)
            next_comb_sets = sorted(
                next_comb_sets, reverse=True, key=lambda cube: len(cube[0]))
            if self.solver(next_comb_sets):
                return True
            self.board[row][col] = 0
        return False

    @staticmethod
    def _get_rand_num(num_possibilities):
        """Helps to determine whether it place number or zero depending on the difficulty level.
        The higher difficulty you get more zeros on the board..

        Args:
            num_possibilities (set{int}): Set that contains all the numbers that can be inserted for given cube..

        Returns:
            int: return the number that will be inserted fir given cube on the sudoku board.
        """
        set_difficulty = 0.7
        num_or_0 = random.random() // set_difficulty
        if num_or_0:
            return random.choice(num_possibilities)
        else:
            return 0

    def sudoku_maker(self, row_sets, col_sets, box_sets):
        """Recursive function that creates new sudoku board.

         Args:
             row_sets (list[set{int}]): Array that contains all the number that can be inserted for each row.
             col_sets (list[set{int}]): Array that contains all the number that can be inserted for each col.
             box_sets (list[set{int}]): Array that contains all the number that can be inserted for each box.

         Returns:
             bool: return True for success or false for failure.
         """
        next_pos = self._find_next_pos()
        if not next_pos:
            return True
        else:
            i, j = next_pos
            box_num = 3 * (i // 3) + j // 3
            if row_sets[i] & col_sets[j] & box_sets[box_num]:
                # check all the possibilities for each number that can be writen.
                num_options = list(
                    row_sets[i] & col_sets[j] & box_sets[box_num])
                for _ in num_options:
                    rand_num = self._get_rand_num(num_options)
                    self.board[i][j] = rand_num
                    if rand_num:
                        row_sets[i].remove(rand_num), col_sets[j].remove(
                            rand_num), box_sets[box_num].remove(rand_num)
                    if self.sudoku_maker(row_sets, col_sets, box_sets):
                        return True
                    self.board[i][j] = '-'
                    if rand_num:
                        row_sets[i].add(rand_num), col_sets[j].add(
                            rand_num), box_sets[box_num].add(rand_num)
            return False

    def __str__(self):
        """Printing the sudoku board"""
        for i, line in enumerate(self.board):
            if i % 3 == 0 and i != 0:
                print('- ' * 11)
            for n, curr_num in enumerate(line):
                if n % 3 == 0 and n != 0:
                    print('|', end=' ')
                print(curr_num, end=' ')
            print()
        return ''

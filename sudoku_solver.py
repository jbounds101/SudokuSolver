import copy
import random


class SudokuBoard:
    def __init__(self, arr=None):
        if arr is None:
            arr = []
            for i in range(9):
                arr.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.arr = arr
        '''
        sub_sections are in the form:
        0 1 2
        3 4 5
        6 7 8
        '''

    def __str__(self):
        if self.arr is None:
            return 'Invalid Board'
        self_string = ''
        for row in range(9):
            for subsection in range(3):
                # The subsection horizontally
                row_string = str(self.arr[row][3 * subsection:(3 * (subsection + 1))])
                row_string = row_string.replace('[', '').replace(']', '').replace(',', '').replace('0', ' ')
                self_string += row_string
                if subsection != 2:
                    self_string += ' | '
            self_string += '\n'
            if row == 2 or row == 5:
                self_string += '-' * 21
                self_string += '\n'
        return self_string

    def solve(self):
        """ Returns the solved array of the SudokuBoard object or None if there are no solutions OR multiple
        solutions (not valid sudoku board) """
        solve_board = SudokuBoard(copy.deepcopy(self.arr))
        if not solve_board.is_valid_config():
            return None
        attempted_nums = []
        for i in range(82):
            attempted_nums.append([])
        solution_stack = []
        initial_solution = []
        solution_found = False

        while True:
            i = 0
            while i < 9:
                j = 0
                while j < 9:
                    if solve_board.arr[i][j] == 0:
                        insert_num = solve_board.__attempt_insert_num(j, i, attempted_nums[(i * 9) + j])
                        if insert_num == -1:
                            # No solution for the current location, pop stack
                            try:
                                popped = solution_stack.pop()
                                j = popped[0]
                                i = popped[1]
                                solve_board.arr[i][j] = 0
                                SudokuBoard.__cleanse_after(i, j, attempted_nums)
                                continue
                            except IndexError:
                                if not solution_found:
                                    return None  # There is no possible solution, the solution_stack was emptied
                                    # without a single solution being found

                                # This must be the solution, the solution_stack is empty
                                self.arr = initial_solution
                                return self
                        else:
                            solution_stack.append([j, i, insert_num])
                            # noinspection PyTypeChecker
                            attempted_nums[(i * 9) + j].append(insert_num)
                    j += 1
                i += 1
            if solution_found:
                # Another solution was found
                return None

            # First solution found, remove the last element and backtrack, see if another solution can be found
            solution_found = True
            # initial_solution is the first solution found, need to copy in case there are no other solutions possible
            initial_solution = copy.deepcopy(solve_board.arr)
            popped = solution_stack.pop()
            j = popped[0]
            i = popped[1]
            solve_board.arr[i][j] = 0
            SudokuBoard.__cleanse_after(i, j, attempted_nums)

    def get_sub_sections(self):
        """ Returns the sub_sections of the sudoku board """
        sections = []
        for section in range(9):
            row_index = {
                0: 0, 1: 0, 2: 0,
                3: 3, 4: 3, 5: 3,
                6: 6, 7: 6, 8: 6
            }[section]
            column_index = {
                0: 0, 1: 3, 2: 6,
                3: 0, 4: 3, 5: 6,
                6: 0, 7: 3, 8: 6
            }[section]
            current_section = [[], [], []]
            for i in range(row_index, row_index + 3):
                for j in range(column_index, column_index + 3):
                    current_section[i - row_index].append(self.arr[i][j])
            sections.append(current_section)
        return sections

    def is_valid_config(self):
        #  Checks self.arr to see if the current array is a valid Sudoku Board
        for row in range(9):
            for column in range(9):
                if self.arr[row][column] != 0:
                    if not self.__valid_insert(column, row, self.arr[row][column]):
                        return False
        return True

    def __attempt_insert_num(self, x, y, ignore_vals):
        """
            Tries to insert a random value 1-9 in the list, if fails, attempt to insert 1-9 minus the already
            attempted num(s)
            If it cannot insert any number, returns None
        """
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(values)
        for i in values:
            if i in ignore_vals:
                continue
            if self.__valid_insert(x, y, i):
                self.arr[y][x] = i
                return i
        return -1

    def __valid_insert(self, x, y, n):
        """ Check if inserting n at (x, y) results in a valid Sudoku board """

        # Go across row and column simultaneously
        for i in range(9):
            if (self.arr[y][i] == n) and (i != x):
                return False
            if (self.arr[i][x] == n) and (i != y):
                return False

        # Check sub_section
        section_num = SudokuBoard.__get_sub_section(x, y)
        row_index = {
            0: 0, 1: 0, 2: 0,
            3: 3, 4: 3, 5: 3,
            6: 6, 7: 6, 8: 6
        }[section_num]
        column_index = {
            0: 0, 1: 3, 2: 6,
            3: 0, 4: 3, 5: 6,
            6: 0, 7: 3, 8: 6
        }[section_num]
        for i in range(row_index, row_index + 3):
            for j in range(column_index, column_index + 3):
                if (i == y) and (j == x):
                    # Skip the value we are looking to change
                    continue
                if self.arr[i][j] == n:
                    return False

        return True

    @staticmethod
    def __cleanse_after(i, j, to_clean):
        """ Removes all values from to_clean (list of lists) after (j, i) """
        start_index = (i * 9) + j + 1
        for i in range(start_index, 82):
            to_clean[i].clear()

    @staticmethod
    def __get_sub_section(x, y):
        """ Returns the sub_section of the given (x,y) coordinate """
        coord = {
            0: 0, 1: 0, 2: 0,
            3: 1, 4: 1, 5: 1,
            6: 2, 7: 2, 8: 2
        }
        row = coord[y]
        column = coord[x]

        return {
            (0, 0): 0, (0, 1): 1, (0, 2): 2,
            (1, 0): 3, (1, 1): 4, (1, 2): 5,
            (2, 0): 6, (2, 1): 7, (2, 2): 8
        }[row, column]

    @staticmethod
    def generate_board(num_squares):
        generated_board = SudokuBoard()
        generated_board.arr = generated_board.solve()
        if num_squares < 17:
            num_squares = 17  # this is the absolute minimum for a sudoku puzzle to be solvable
        if num_squares > 81:
            return generated_board

        remaining_spots = []
        for row in range(9):
            for column in range(9):
                remaining_spots.append([row, column])
        random.shuffle(remaining_spots)

        squares_to_erase = 81 - num_squares
        for i in range(squares_to_erase):
            row = remaining_spots[0][0]
            column = remaining_spots[0][1]
            remaining_spots.pop(0)
            generated_board.arr[row][column] = 0

        return generated_board


sudoku_arr = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

other_sudoku_arr = [
    [0, 7, 5, 0, 9, 0, 0, 0, 6],
    [0, 2, 3, 0, 8, 0, 0, 4, 0],
    [8, 0, 0, 0, 0, 3, 0, 0, 1],
    [5, 0, 0, 7, 0, 2, 0, 0, 0],
    [0, 4, 0, 8, 0, 6, 0, 2, 0],
    [0, 0, 0, 9, 0, 1, 0, 0, 3],
    [9, 0, 0, 4, 0, 0, 0, 0, 7],
    [0, 6, 0, 0, 7, 0, 5, 8, 0],
    [7, 0, 0, 0, 1, 0, 3, 9, 0]
]

two_solution_arr = [
    [2, 9, 5, 7, 4, 3, 8, 6, 1],
    [4, 3, 1, 8, 6, 5, 9, 0, 0],
    [8, 7, 6, 1, 9, 2, 5, 4, 3],
    [3, 8, 7, 4, 5, 9, 2, 1, 6],
    [6, 1, 2, 3, 8, 7, 4, 9, 5],
    [5, 4, 9, 2, 1, 6, 7, 3, 8],
    [7, 6, 3, 5, 2, 4, 1, 8, 9],
    [9, 2, 8, 6, 7, 1, 3, 5, 4],
    [1, 5, 4, 9, 3, 8, 6, 0, 0]
]

unsolvable_sudoku_arr = [
    [5, 1, 6, 8, 4, 9, 7, 3, 2],
    [3, 0, 7, 6, 0, 5, 0, 0, 0],
    [8, 0, 9, 7, 0, 0, 0, 6, 5],
    [1, 3, 5, 0, 6, 0, 9, 0, 7],
    [4, 7, 2, 5, 9, 1, 0, 0, 6],
    [9, 6, 8, 3, 7, 0, 0, 5, 0],
    [2, 5, 3, 1, 8, 6, 0, 7, 4],
    [6, 8, 4, 2, 0, 7, 5, 0, 0],
    [7, 9, 1, 0, 5, 0, 6, 0, 8]
]

bad_board = SudokuBoard(unsolvable_sudoku_arr)
print(bad_board.solve())

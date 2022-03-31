import copy


class SudokuBoard:
    def __init__(self, arr):
        self.arr = arr

        '''
        sub_sections are in the form:
        0 1 2
        3 4 5
        6 7 8
        '''
        self.sub_sections = []

    def __str__(self):
        self_string = ''
        for i in range(9):
            for j in range(9):
                # i = row, j = column
                pass  # todo finish

    def solve(self):
        solve_board = SudokuBoard(copy.deepcopy(self.arr))
        attempted_nums = []
        for i in range(82):
            attempted_nums.append([])

        solution_stack = []
        i = 0
        while i < 9:
            j = 0
            while j < 9:
                if solve_board.arr[i][j] == 0:
                    insert_num = solve_board.attempt_insert_num(j, i, attempted_nums[(i * 9) + j])
                    if insert_num == -1:
                        # No solution for the current location, pop stack
                        popped = solution_stack.pop()
                        j = popped[0]
                        i = popped[1]
                        solve_board.arr[i][j] = 0
                        SudokuBoard.cleanse_attempted_after(i, j, attempted_nums)

                        continue
                    else:
                        solution_stack.append([j, i, insert_num])
                        attempted_nums[(i * 9) + j].append(insert_num)
                j += 1
            i += 1
        return solve_board

    def attempt_insert_num(self, x, y, ignore_vals):
        """
            Tries to insert 1 in the location specified, if it cannot, tries 2 ...
            If it cannot insert any number, returns None
        """
        for i in range(1, 10):
            if i in ignore_vals:
                continue
            if self.valid_insert(x, y, i):
                self.arr[y][x] = i
                return i
        return -1

    def valid_insert(self, x, y, n):
        """ Check if inserting n at (x, y) results in a valid Sudoku board """

        # Go across row and column simultaneously
        for i in range(9):
            if (self.arr[y][i] == n) and (i != x):
                return False
            if (self.arr[i][x] == n) and (i != y):
                return False

        # Check sub_section
        self.sub_sections = self.get_sub_sections()
        section_num = SudokuBoard.get_sub_section(x, y)
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

    @staticmethod
    def cleanse_attempted_after(i, j, to_clean):
        """ Removes all values of attempted_nums after (j, i) """
        start_index = (i * 9) + j + 1
        for i in range(start_index, 82):
            to_clean[i].clear()

    @staticmethod
    def get_sub_section(x, y):
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


sudokuArr = [
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
sudoku_board = SudokuBoard(sudokuArr)
sudoku_board.solve()

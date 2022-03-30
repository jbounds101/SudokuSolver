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

    def valid(self, x, y, n):
        check_arr = copy.deepcopy(self.arr)
        check_arr[x][y] = n
        self.sub_sections = SudokuBoard.get_sub_sections(self)

    @staticmethod
    def get_sub_sections(board):
        """ Returns the sub_sections of the sudoku board """
        sections = []
        for section in range(9):
            column_index = {
                0: 0, 1: 3, 2: 6,
                3: 0, 4: 3, 5: 6,
                6: 0, 7: 3, 8: 6
            }[section]
            row_index = {
                0: 0, 1: 0, 2: 0,
                3: 3, 4: 3, 5: 3,
                6: 6, 7: 6, 8: 6
            }[section]
            current_section = [[], [], []]
            for i in range(row_index, row_index + 3):
                for j in range(column_index, column_index + 3):
                    current_section[i - row_index].append(board.arr[i][j])
            sections.append(current_section)
        return sections

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
            (0, 0): 0, (0, 1): 2, (0, 2): 3,
            (1, 0): 4, (1, 1): 5, (1, 2): 6,
            (2, 0): 7, (2, 1): 8, (2, 2): 9,
        }[row, column]


arr = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
       [6, 0, 0, 1, 9, 5, 0, 0, 0],
       [0, 9, 8, 0, 0, 0, 0, 6, 0],
       [8, 0, 0, 0, 6, 0, 0, 0, 3],
       [4, 0, 0, 8, 0, 3, 0, 0, 1],
       [7, 0, 0, 0, 2, 0, 0, 0, 6],
       [0, 6, 0, 0, 0, 0, 2, 8, 0],
       [0, 0, 0, 4, 1, 9, 0, 0, 5],
       [0, 0, 0, 0, 8, 0, 0, 7, 9]]
board = SudokuBoard(arr)
board.valid(0, 0, 0)

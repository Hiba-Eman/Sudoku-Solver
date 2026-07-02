class SudokuSolver:

    def __init__(self, board):
        self.board = board
    
    def find_empty(self):

        for row in range(9):
            for col in range(9):

                if self.board[row][col] == 0:
                    return row, col

        return None
    
    def is_valid(self, number, position):

        row, col = position

        # Check row
        for i in range(9):
            if self.board[row][i] == number and i != col:
                return False

        # Check column
        for i in range(9):
            if self.board[i][col] == number and i != row:
                return False

        # Check 3x3 box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3

        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] == number and (i, j) != position:
                    return False

        return True
    def solve(self):

        empty = self.find_empty()

        if empty is None:
            return True

        row, col = empty

        for number in range(1, 10):

            if self.is_valid(number, (row, col)):

                self.board[row][col] = number

                if self.solve():
                    return True

                self.board[row][col] = 0

        return False
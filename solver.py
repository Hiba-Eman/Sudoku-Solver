class SudokuSolver:
    """
    Backtracking Sudoku solver.

    - solve()          -> fast, non-animated solve (mutates self.board in place)
    - solve_animated()  -> generator version that yields a step at a time so a
                            GUI can visualize the algorithm (try / place / backtrack)
    """

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

    def solve_animated(self):
        """
        Generator that yields tuples of (action, row, col, value) so the GUI can
        animate the backtracking algorithm.

        action is one of:
            "try"        -> about to test `value` at (row, col)
            "place"      -> `value` is valid and has been placed at (row, col)
            "backtrack"  -> the placement failed further down the tree and the
                             cell has been cleared back to 0

        Returns True/False (accessible via the StopIteration value when the
        generator is exhausted) indicating whether the board was solved.
        """
        empty = self.find_empty()

        if empty is None:
            return True

        row, col = empty

        for number in range(1, 10):
            yield ("try", row, col, number)

            if self.is_valid(number, (row, col)):
                self.board[row][col] = number
                yield ("place", row, col, number)

                result = yield from self.solve_animated()
                if result:
                    return True

                self.board[row][col] = 0
                yield ("backtrack", row, col, 0)

        return False
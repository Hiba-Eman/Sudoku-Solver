import random

class SudokuGenerator:

    DIFFICULTY_REMOVALS = {
        "easy": 36,
        "medium": 46,
        "hard": 54,
    }

    def __init__(self):
        self.board = [[0] * 9 for _ in range(9)]

    def generate_full_board(self):
        self.board = [[0] * 9 for _ in range(9)]
        self._fill_board()
        return [row[:] for row in self.board]

    def _fill_board(self):
        empty = self._find_empty(self.board)

        if empty is None:
            return True

        row, col = empty
        numbers = list(range(1, 10))
        random.shuffle(numbers)

        for number in numbers:
            if self._is_valid(self.board, number, row, col):
                self.board[row][col] = number

                if self._fill_board():
                    return True

                self.board[row][col] = 0

        return False

    def _find_empty(self, board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    return row, col
        return None

    def _is_valid(self, board, number, row, col):
        for i in range(9):
            if board[row][i] == number or board[i][col] == number:
                return False

        box_row = (row // 3) * 3
        box_col = (col // 3) * 3

        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == number:
                    return False

        return True

    def generate_puzzle(self, difficulty="medium"):

        full_board = self.generate_full_board()
        puzzle = [row[:] for row in full_board]

        cells_to_remove = self.DIFFICULTY_REMOVALS.get(difficulty, 46)

        positions = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(positions)

        for row, col in positions[:cells_to_remove]:
            puzzle[row][col] = 0

        return puzzle, full_board
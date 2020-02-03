import math
from enum import Enum
from random import choices


class CellState(Enum):
    COVERED = 1
    UNCOVERED = 2
    MARKED = 3


class GameState(Enum):
    IN_PROGRESS = 1
    LOST = 2
    WON = 3


class UnableToFlipException(Exception):
    def __init__(self, *args, cell_state):
        super().__init__(args)
        self.cell_state = cell_state


class GameOverException(Exception):
    def __init__(self, *args, state):
        super().__init__(args)
        self.state = state


class GameLostException(GameOverException):
    def __init__(self, *args):
        super().__init__(args, state=GameState.LOST)


class VoltorbFlip:

    available_values = [0, 1, 2, 3]
    available_weights = [0.15, 0.5, 0.15, 0.1]

    @staticmethod
    def _generate_board(width, height):
        return [
            [
                choices(VoltorbFlip.available_values, VoltorbFlip.available_weights)[0]
                for _ in range(width)
            ]
            for _ in range(height)
        ]

    @staticmethod
    def _generate_states(width, height):
        return [[CellState.COVERED for _ in range(width)] for _ in range(height)]

    @staticmethod
    def _calculate_borders(board):
        height = len(board)
        width = len(board[0])

        horizontal_points = [sum(arr) for arr in board]
        horizontal_bombs = [0 for _ in range(height)]
        for row, arr in enumerate(board):
            for value in arr:
                if value == 0:
                    horizontal_bombs[row] += 1

        vertical_points = [0 for _ in range(width)]
        vertical_bombs = [0 for _ in range(width)]
        for i in range(width):
            for j in range(height):
                vertical_points[i] += board[j][i]
                if board[i][j] == 0:
                    vertical_bombs[j] += 1

        return horizontal_points, horizontal_bombs, vertical_points, vertical_bombs

    @staticmethod
    def _calculate_winning_score(board):
        score = 1
        for row in board:
            for number in row:
                score *= 1 if number == 0 else number
        return score

    def __init__(self, width=5, height=5):
        self.width = width
        self.height = height
        self.score = 1
        self.state = GameState.IN_PROGRESS
        self.board = self._generate_board(width, height)
        self.cell_states = VoltorbFlip._generate_states(width, height)
        (
            self.horizontal_points,
            self.horizontal_bombs,
            self.vertical_points,
            self.vertical_bombs,
        ) = VoltorbFlip._calculate_borders(self.board)
        self.maximum_points = VoltorbFlip._calculate_winning_score(self.board)

    def mark(self, row, column):
        self._change_cell_state(row, column, CellState.MARKED)

    def unmark(self, row, column):
        self._change_cell_state(row, column, CellState.COVERED)

    def flip(self, row, column):
        if self.state != GameState.IN_PROGRESS:
            raise GameOverException(state=self.state)

        if self.cell_states[row][column] != CellState.COVERED:
            raise UnableToFlipException(cell_state=self.cell_states[row][column])

        self._change_cell_state(row, column, CellState.UNCOVERED)
        self.score *= self.board[row][column]

        self._win_or_lose()

    def _win_or_lose(self):
        if self.score == self.maximum_points:
            self.state = GameState.WON
        elif self.score == 0:
            self.state = GameState.LOST
            raise GameLostException()

    def _change_cell_state(self, row, column, new_state):
        if self.cell_states[row][column] == CellState.UNCOVERED:
            return
        self.cell_states[row][column] = new_state

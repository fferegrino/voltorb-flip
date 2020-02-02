from enum import Enum
from random import choices


class CellState(Enum):
    COVERED = 1
    UNCOVERED = 2
    MARKED = 3


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

    def __init__(self, width=5, height=5):
        self.width = width
        self.height = height
        self.score = 1
        self.is_finished = False
        self.board = self._generate_board(width, height)
        self.cell_states = VoltorbFlip._generate_states(width, height)
        (
            self.horizontal_points,
            self.horizontal_bombs,
            self.vertical_points,
            self.vertical_bombs,
        ) = VoltorbFlip._calculate_borders(self.board)

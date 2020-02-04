import re

import click

from voltorb_flip.game import (
    CellState,
    GameLostException,
    GameState,
    UnableToFlipException,
    VoltorbFlip,
)

COVERED_CHARACTER = "?"
MARKED_CHARACTER = "M"
COMMAND_REGEX = re.compile(r"([fmq])(?:([a-z])([\d]))?")


class ConsoleGame:
    def __init__(self, level, width, height):
        self.game = VoltorbFlip(level=level, width=width, height=height)
        self.latest_error = None

    def get_board(self):
        game = self.game
        game_string = []
        headers_row = "      ".join([str(column + 1) for column in range(game.width)])
        game_string.append(" " * 6 + headers_row)
        for row in range(game.height):
            row_str = ""
            current_row_label = chr(ord("a") + row)
            row_str = row_str + f"{current_row_label:>3}"
            for column in range(game.width):
                value = ConsoleGame._get_cell_value(column, game, row)
                row_str = row_str + f" [ {value} ] "
            row_str = (
                row_str + f" {game.horizontal_points[row]}/{game.horizontal_bombs[row]}"
            )
            game_string.append(row_str)
        ver_stats_row = "    ".join(
            [
                f"{game.vertical_points[column]}/{game.vertical_bombs[column]}"
                for column in range(game.width)
            ]
        )
        game_string.append(" " * 5 + ver_stats_row)
        game_string = [string.ljust(45, " ") for string in game_string]
        return game_string

    def draw_game(self):
        click.clear()
        board_string = self.get_board()
        print("\n".join(board_string))

    def _process_command(self, command):
        action = re.match(COMMAND_REGEX, command)
        if not action:
            return True
        action, row, column = action.groups()
        if action == "q":
            return False

        actual_row = ord(row) - ord("a")
        actual_column = int(column) - 1

        if action == "f":
            self.game.flip(actual_row, actual_column)
        elif action == "m":
            self.game.toggle_mark(actual_row, actual_column)

        return self.game.state == GameState.IN_PROGRESS

    def process_input(self):
        print(f"Error! {self.latest_error}" if self.latest_error else "")
        print("Please enter your command:")
        command_input = input()  # nosec
        try:
            self.latest_error = None
            return self._process_command(command_input)
        except UnableToFlipException as flip_excp:
            self.latest_error = (
                f"That cell can't be uncovered, it is {flip_excp.cell_state.name}"
            )
            return True
        except GameLostException:
            return False

        return True

    @staticmethod
    def _get_cell_value(column, game, row):
        cell_state = game.cell_states[row][column]
        value = str(game.board[row][column])
        if cell_state == CellState.COVERED:
            value = COVERED_CHARACTER
        elif cell_state == CellState.MARKED:
            value = MARKED_CHARACTER
        return value

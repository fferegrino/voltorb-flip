import re

import click
from rich import box, print
from rich.console import Console
from rich.style import Style
from rich.table import Table
from rich.theme import Theme

# fmt: off
from voltorb_flip.game import (
    CellState,
    GameState,
    UnableToFlipException,
    VoltorbFlip,
)

# fmt: on

THEME = Theme({"card": "dim cyan", "bomb": "red",
               "flipped_good": Style(color="white", bgcolor="#309f6a"),
               "covered": Style(color="#309f6a", bgcolor="#309f6a")
               })

COVERED_CHARACTER = "?"
MARKED_CHARACTER = "M"
COMMAND_REGEX = re.compile(r"([fmq])(?:([a-z])([\d]))?")


class ConsoleGame:
    def __init__(self):
        self.game = VoltorbFlip()
        self.latest_error = None
        self.console = Console(theme=THEME)

    def get_board(self):
        table = Table(box=box.ROUNDED)

        # Columns
        table.add_column(" ")
        for row in range(self.game.CLASSIC_BOARD_SIZE):
            table.add_column(str(row + 1))
        table.add_column("😬")
        table.add_column("💣")

        # Rows
        for row in range(self.game.CLASSIC_BOARD_SIZE):
            current_row_label = chr(ord("a") + row)
            column_elements = [current_row_label]
            for column in range(self.game.CLASSIC_BOARD_SIZE):
                value = ConsoleGame._get_cell_value(column, self.game, row)

                if value.isnumeric():
                    value = f"[flipped_good]{value}[/flipped_good]"
                elif value == COVERED_CHARACTER:
                    value = f"[covered]{value}[/covered]"

                column_elements.append(value)

            column_elements.append(f"{self.game.vertical_points[row]}")
            column_elements.append(f"[bomb]{self.game.vertical_bombs[row]}[/bomb]")
            table.add_row(*column_elements)

        # Last row
        column_elements = ["😬\n💣"]
        for row in range(self.game.CLASSIC_BOARD_SIZE):
            column_elements.append(
                f"{self.game.horizontal_points[row]}\n[bomb]{self.game.horizontal_bombs[row]}[/bomb]"
            )
        column_elements.append("")
        table.add_row(*column_elements)

        return table

    def draw_game(self):
        self.console.clear()
        board_string = self.get_board()
        self.console.print(board_string)
        self.console.print(f"Current score {self.game.current_score}")

    def _process_command(self, command):
        action = re.match(COMMAND_REGEX, command)
        if not action:
            self.latest_error = f'"{command}" is not a valid command!'
            return True
        action, row, column = action.groups()
        if action == "q":
            return False

        actual_row = ord(row) - ord("a")
        actual_column = int(column) - 1

        if action == "f":
            self.game.flip(actual_row, actual_column)

        return self.game.state == GameState.IN_PROGRESS

    def process_input(self):
        self.console.print(f"Error! {self.latest_error}" if self.latest_error else "")
        self.console.print()
        self.console.print("Commands structure:")
        self.console.print(" - q: quit game")
        self.console.print(" - fXY: flip cell X,Y where X is a letter and Y is a number")
        self.console.print(" - mXY: mark cell X,Y where X is a letter and Y is a number")
        self.console.print("Please enter your command:")
        command_input = input()  # nosec
        try:
            self.latest_error = None
            return self._process_command(command_input)
        except UnableToFlipException as flip_excp:
            self.latest_error = f"That cell can't be uncovered, it is {flip_excp.cell_state.name}"
            return True

        return True

    @staticmethod
    def _get_cell_value(column, game, row):
        cell_state = game.cell_states[row][column]
        value = str(game.board[row][column])
        if cell_state == CellState.COVERED:
            value = COVERED_CHARACTER
        elif cell_state != CellState.UNCOVERED:
            value = MARKED_CHARACTER
        return value

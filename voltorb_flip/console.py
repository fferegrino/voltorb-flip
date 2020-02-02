from voltorb_flip.game import CellState

COVERED_CHARACTER = "X"
MARKED_CHARACTER = "M"


def draw_game(game):
    headers_row = "      ".join([str(column + 1) for column in range(game.width)])
    print(" " * 6 + headers_row)
    for row in range(game.height):
        current_row_label = chr(ord("a") + row)
        print(f"{current_row_label:>3}", end="")
        for column in range(game.width):
            value = _get_cell_value(column, game, row)
            print(f" [ {value} ] ", end="")
        else:
            print(f" {game.horizontal_points[row]}/{game.horizontal_bombs[row]}")
    else:
        ver_stats_row = "    ".join(
            [
                f"{game.vertical_points[column]}/{game.vertical_bombs[column]}"
                for column in range(game.width)
            ]
        )
        print(" " * 5 + ver_stats_row)


def _get_cell_value(column, game, row):
    cell_state = game.cell_states[row][column]
    value = str(game.board[row][column])
    if cell_state == CellState.COVERED:
        value = COVERED_CHARACTER
    elif cell_state == CellState.MARKED:
        value = MARKED_CHARACTER
    return value

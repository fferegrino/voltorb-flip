import pytest
from unittest.mock import patch

from voltorb_flip.game import (
    VoltorbFlip,
    GameState,
    GameLostException,
    GameOverException,
)


@pytest.mark.parametrize(
    ["board", "moves"],
    [
        # fmt: off
        (
            [[1, 2, 0],
             [0, 3, 1],
             [1, 0, 0]],

            [(0, 0), (0,1), (1,1)]
        ),
        (
            [[0, 1, 2, 3, 0],
             [1, 0, 0, 0, 3],
             [1, 0, 0, 3, 1],
             [1, 3, 0, 2, 1],
             [3, 1, 1, 2, 0]],

            [(0, 2), (0, 3), (1, 4), (2, 3), (3, 1), (3, 3), (4, 3), (4, 0)]
        )
        # fmt: on
    ],
)
@patch("voltorb_flip.game.VoltorbFlip._generate_board")
def test_win(generate_board_mock, board, moves):
    generate_board_mock.return_value = board
    height = len(board)
    width = len(board[0])

    game = VoltorbFlip(width=width, height=height)

    assert game.state == GameState.IN_PROGRESS
    for i, j in moves:
        game.flip(i, j)
    assert game.state == GameState.WON

    generate_board_mock.assert_called_once_with(width, height)


@pytest.mark.parametrize(
    ["board", "moves"],
    [
        # fmt: off
        (
            [[1, 2, 0],
             [0, 3, 1],
             [1, 0, 0]],

            [(0, 0), (0,1), (1,1)]
        ),
        (
            [[0, 1, 2, 3, 0],
             [1, 0, 0, 0, 3],
             [1, 0, 0, 3, 1],
             [1, 3, 0, 2, 1],
             [3, 1, 1, 2, 0]],

            [(0, 2), (0, 3), (1, 4), (2, 3), (3, 1), (3, 3), (4, 3), (4, 0)]
        )
        # fmt: on
    ],
)
@patch("voltorb_flip.game.VoltorbFlip._generate_board")
def test_cant_play_game_over(generate_board_mock, board, moves):
    generate_board_mock.return_value = board
    height = len(board)
    width = len(board[0])

    game = VoltorbFlip(width=width, height=height)

    assert game.state == GameState.IN_PROGRESS
    for i, j in moves:
        game.flip(i, j)
    with pytest.raises(GameOverException) as excp:
        game.flip(0, 0)
        assert excp.state == GameState.WON
    assert game.state == GameState.WON

    generate_board_mock.assert_called_once_with(width, height)


@pytest.mark.parametrize(
    ["board", "moves"],
    [
        # fmt: off
        (
            [[1, 2, 0],
             [0, 3, 1],
             [1, 0, 0]],

            [(0, 0), (0,1), (1,0)]
        ),
        (
            [[0, 1, 2, 3, 0],
             [1, 0, 0, 0, 3],
             [1, 0, 0, 3, 1],
             [1, 3, 0, 2, 1],
             [3, 1, 1, 2, 0]],

            [(0, 2), (0, 3), (0, 0)]
        )
        # fmt: on
    ],
)
@patch("voltorb_flip.game.VoltorbFlip._generate_board")
def test_lose(generate_board_mock, board, moves):
    generate_board_mock.return_value = board
    height = len(board)
    width = len(board[0])

    game = VoltorbFlip(width=width, height=height)

    assert game.state == GameState.IN_PROGRESS
    for i, j in moves[:-1]:
        game.flip(i, j)
    with pytest.raises(GameLostException):
        i, j = moves[-1]
        game.flip(i, j)
    assert game.state == GameState.LOST

    generate_board_mock.assert_called_once_with(width, height)

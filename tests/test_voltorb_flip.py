import pytest
from unittest.mock import patch
from voltorb_flip.game import VoltorbFlip, CellState


@pytest.fixture
def patched_init():
    with patch.object(VoltorbFlip, "__init__", lambda _, width, height: None):
        yield


@pytest.mark.parametrize("width", [2, 5])
@pytest.mark.parametrize("height", [2, 5])
def test_creates_board(width, height):

    board = VoltorbFlip._generate_board(width, height)
    assert len(board) == height
    assert len(board[0]) == width
    assert isinstance(board[0][0], int)


@pytest.mark.parametrize("width", [2, 5])
@pytest.mark.parametrize("height", [2, 5])
def test_sets_states(patched_init, width, height):

    states = VoltorbFlip._generate_states(width, height)

    assert len(states) == height
    assert len(states[0]) == width
    assert all(
        [
            all([state == CellState.COVERED for state in states[i]])
            for i in range(height)
        ]
    )


@pytest.mark.parametrize(
    ["board", "points"],
    [
        # fmt: off
        (
            [[1, 2, 0],
             [0, 3, 1],
             [1, 0, 0]],

            6
        ),
        (
            [[0, 1, 2, 3, 0],
             [1, 0, 0, 0, 3],
             [1, 0, 0, 3, 1],
             [1, 3, 0, 2, 1],
             [3, 1, 1, 2, 0]],

            1944
        )
        # fmt: on
    ],
)
def test_calculate_max_points(board, points):
    actual = VoltorbFlip._calculate_winning_score(board)
    assert actual == points


@pytest.mark.parametrize(
    ["board", "hpoints", "hbombs", "vpoints", "vbombs"],
    [
        # fmt: off
        (
            [[1, 2, 0],
             [0, 3, 1],
             [1, 0, 0]],

            [3, 4, 1], [1, 1, 2], [2, 5, 1], [1, 1, 2]
        ),
        (
            [[0, 1, 2, 3, 0],
             [1, 0, 0, 0, 3],
             [1, 0, 0, 3, 1],
             [1, 3, 0, 2, 1],
             [3, 1, 1, 2, 0]],

            [6, 4, 5, 7, 7], [2, 3, 2, 1, 1], [6, 5, 3, 10, 5], [1, 2, 3, 1, 2]
        )
        # fmt: on
    ],
)
def test_calculate_borders(board, hpoints, hbombs, vpoints, vbombs):
    actual_hpoints, actual_hbombs, actual_vpoints, actual_vbombs = VoltorbFlip._calculate_borders(
        board
    )
    assert actual_hbombs == hbombs
    assert actual_hpoints == hpoints
    assert actual_vbombs == vbombs
    assert actual_vpoints == vpoints

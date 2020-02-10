import pytest

from voltorb_flip.levels import CLASSIC_LEVELS, generate_board


def test_levels():
    for level, configurations in CLASSIC_LEVELS.items():
        for points, x2, x3, _ in configurations:
            assert points == (3 ** x3) * (2 ** x2)


@pytest.mark.parametrize("level", [i + 1 for i in range(8)])
def test_generate_board(level):
    board = generate_board(level)
    assert len(board) == 5
    for row in board:
        assert len(row) == 5

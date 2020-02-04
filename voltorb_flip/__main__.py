import click

from voltorb_flip.console import ConsoleGame


@click.group()
def cli():
    pass


@cli.command()
@click.option("-l", "--level", "level", type=int, default=1)
@click.option("-w", "--width", "width", type=int, default=5)
@click.option("-h", "--height", "height", type=int, default=5)
def new(level, width, height):
    game = ConsoleGame(level, width, height)
    still_playing = True
    while still_playing:
        game.draw_game()
        still_playing = game.process_input()


@cli.command()
def help():
    print(
        """
    Every box contains a value, from 0 to 3.
    Each time you discover a new number, your score gets multiplied by it (first one is multiplied by 1 of course).
    If you discover 2 or 3, you get more points. 1, you get nothing more. And if you find a 0, the game is over.
    You win the game when you discovered all 2 and 3 boxes. You can also stop the game to win your current score.
    If you win the game by discovering all 2 and 3, you get to the next level. If you fail too many times, you can fall to lower levels.
    Each level is more difficult than the previous, but you also get more points. There is a maximum of 7 levels.
    Numbers at the end shows the sum of all numbers in the row/column (top), and how much zeroes there are (bottom).
"""
    )


if __name__ == "__main__":
    # pylint: disable=E1120
    cli()

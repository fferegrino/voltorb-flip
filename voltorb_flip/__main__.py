import click

from voltorb_flip.console import draw_game
from voltorb_flip.game import VoltorbFlip


@click.group()
def cli():
    pass


@cli.command()
def new():
    game = VoltorbFlip()
    draw_game(game)


if __name__ == "__main__":
    # pylint: disable=E1120
    cli()

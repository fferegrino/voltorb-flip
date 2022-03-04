import click

from voltorb_flip.console import ConsoleGame
from voltorb_flip.game import GameState


@click.group()
def cli():
    pass


@cli.command()
def new():
    cg = ConsoleGame()

    while cg.game.state == GameState.IN_PROGRESS:
        cg.draw_game()
        cg.process_input()

    cg.draw_game()
    pass


if __name__ == "__main__":
    # pylint: disable=E1120
    cli()

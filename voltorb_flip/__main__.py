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
        if cg.game.state == GameState.WON:
            cg.game.bump_level()
        if cg.game.state == GameState.LOST:
            cg.game.remove_level()

    cg.draw_game()
    pass


if __name__ == "__main__":
    # pylint: disable=E1120
    cli()

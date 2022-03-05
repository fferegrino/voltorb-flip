import click

from voltorb_flip.console import ConsoleGame
from voltorb_flip.game import GameState


@click.group()
def cli():
    pass


@cli.command()
def new():
    console_game = ConsoleGame()

    while console_game.game.state == GameState.IN_PROGRESS:
        console_game.draw_game()
        console_game.process_input()
        if console_game.game.state == GameState.WON:
            console_game.game.bump_level()
        if console_game.game.state == GameState.LOST:
            console_game.game.remove_level()

    console_game.draw_game()


if __name__ == "__main__":
    # pylint: disable=E1120
    cli()

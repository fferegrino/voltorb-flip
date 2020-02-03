import click

from voltorb_flip.console import ConsoleGame


@click.group()
def cli():
    pass


@cli.command()
@click.option("-w", "--width", "width", type=int, default=5)
@click.option("-h", "--height", "height", type=int, default=5)
def new(width, height):
    game = ConsoleGame(width, height)
    still_playing = True
    while still_playing:
        game.draw_game()
        still_playing = game.process_input()


if __name__ == "__main__":
    # pylint: disable=E1120
    cli()

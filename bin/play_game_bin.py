from os import makedirs

import typer

from bojio.game_engine.core.Game import StandardGame

app = typer.Typer()


@app.command()
def bots():
    """Let two bots go head-to-head!"""
    game = StandardGame()
    makedirs("out_files", exist_ok=True)
    game.print_game_state("white", out_file="out_files/move_000.jpg")
    for i in range(1, 201):
        game.tick()
        game.print_game_state("white", out_file=str("out_files/move_%03d.jpg" % (i)))


@app.command()
def interactive(human_player: str = "white"):
    """Play chess in an interactive mode against a bot."""
    game = StandardGame()
    game.print_game_state(human_player, out_file="interactive_game_state.jpg")

    whose_turn = "white"

    while True:
        if whose_turn == human_player:
            move = input("> ")
            if move == "q()":
                print("%s resigned!" % (human_player))
                break
        else:
            pass


def _main():
    app()

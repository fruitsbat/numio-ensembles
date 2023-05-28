#!/usr/bin/env python

import time
import typer
import logging
from rich.logging import RichHandler
from click import Context
from config import MODE, LOGLEVEL
from typing_extensions import Annotated
from typing import Iterable
from rich.progress import track
from typer.core import TyperGroup


# return commands in a more reasonable order than alphabetical
class OrderCommands(TyperGroup):
    def list_commands(self, ctx: Context):
        return list(self.commands)  # return commands in order of appearance


app = typer.Typer(cls=OrderCommands)


@app.command()
def simple(
    load: Annotated[
        MODE,
        typer.Option(
            "--mode",
            "-m",
            help=("what type of load to use, gets overridden by other cli args."),
        ),
    ] = MODE.EMPTY.value
):
    """
    this mode offers preconfigured options.
    use this to run a set of sensible, preconfigured benchmarks.
    """
    print(load)


@app.command()
def advanced():
    """
    this mode offers some options.
    use this if you would like to tweak the script a bit.
    """
    pass


@app.command()
def expert():
    """
    in this mode, the script tries to get out of your way!
    use this if you want to configure everything yourself.
    """
    pass


@app.callback()
def main(
    loglevel: Annotated[
        LOGLEVEL,
        typer.Option("--loglevel", "-l", help="adjust chattyness of app"),
    ] = LOGLEVEL.INFO.value
):
    """
    this is a script designed to help you quickly run numio benchmarks.
    it tries to simulate realistic test conditions by creating disk and network load.
    these are shared resources, so performance issues related to them would be hard to find using an isolated program.

    """
    loglevel.init_logging()


if __name__ == "__main__":
    app()

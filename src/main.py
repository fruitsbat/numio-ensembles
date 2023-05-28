#!/usr/bin/env python

import time
import typer
import logging
from rich.logging import RichHandler
from config import MODE, LOGLEVEL
from typing_extensions import Annotated
from rich.progress import track

app = typer.Typer()


# run a test
@app.command()
def run(
    load: Annotated[
        MODE,
        typer.Option(
            "--mode",
            "-m",
            help=("what type of load to use, gets overridden by other cli args."),
        ),
    ] = MODE.EMPTY.value
):
    print(load)


@app.callback()
def main(
    loglevel: Annotated[
        LOGLEVEL,
        typer.Option("--loglevel", "-l", help="adjust chattyness of app"),
    ] = LOGLEVEL.INFO
):
    loglevel.init_logging()


if __name__ == "__main__":
    app()

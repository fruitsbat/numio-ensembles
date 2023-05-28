#!/usr/bin/env python

import time
import typer
import logging
from typing_extensions import Annotated
from rich.progress import track

app = typer.Typer()


@app.command()
def easy(wait: Annotated[int, typer.Argument(help="how many seconds to wait")]):
    for value in track(range(wait), description="doing the thing"):
        time.sleep(1)


@app.command()
def advanced():
    logging.info("running advanced example...")


if __name__ == "__main__":
    logging.info("warming up...")
    app()

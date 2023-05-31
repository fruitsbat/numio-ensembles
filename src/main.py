#!/usr/bin/env python
"""
hehe
"""

import time
from pathlib import Path
from rich.progress import Progress, SpinnerColumn, TextColumn
from typer.core import TyperGroup
import typer
from click import Context
from typing_extensions import Annotated
from config import LOGLEVEL
import advanced
import batch
import global_vars


# return commands in a more reasonable order than alphabetical
class OrderCommands(TyperGroup):
    """
    used to order commands in the help prompt in order of appearance
    instead of alphabetically
    """

    def list_commands(self, ctx: Context):
        return list(self.commands)  # return commands in order of appearance


app = typer.Typer(cls=OrderCommands)


@app.command()
def simple():
    """
    This performs a benchmark run
    with sensible defaults.
    Use this if you just want to
    quickly run your benchmark.
    """
    with Progress(
        SpinnerColumn(),
        TextColumn(""),
        transient=True,
    ) as progress:
        progress.print("spinning up!")
        script: batch.BatchScript = batch.BatchScript()
        script.run()
        time.sleep(1)


app.add_typer(
    advanced.app,
    name="advanced",
    help="This performs a configurable benchmark run."
    + " "
    + "Use this if you want more fine grained control of the script.",
)


@app.callback()
def main(
    loglevel: Annotated[
        LOGLEVEL,
        typer.Option("--loglevel", "-l", help="adjust chattyness of app"),
    ] = LOGLEVEL.INFO.value,
    srun_path: Annotated[
        Path,
        typer.Option(
            "--srun-path",
            "-sr",
            help="what command to use for srun",
        ),
    ] = "srun",
    sbatch_path: Annotated[
        Path,
        typer.Option(
            "--sbatch-path",
            "-sb",
            help="what command to use for sbatch",
        ),
    ] = "sbatch",
):
    """
    this is a script designed to help you quickly run numio benchmarks.
    it tries to simulate realistic test conditions
    by creating disk and network load.
    these are shared resources,
    so performance issues related to them would be hard to find
    using an isolated program.

    """
    loglevel.init_logging()
    global_vars.SRUN_PATH = srun_path
    global_vars.SBATCH_PATH = sbatch_path


if __name__ == "__main__":
    app()
